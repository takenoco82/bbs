FROM python:3.7.5-alpine

# change timezone
RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del tzdata

# install develop packages
RUN apk add --no-cache --virtual=develop-deps \
        bash \
        docker \
        git \
        jq \
        less \
        make \
        openssh \
        vim \
        zsh
# install awscli
RUN apk add --no-cache --virtual=awscli-deps groff && \
    pip install --upgrade pip && \
    pip install --no-cache-dir awscli

# install terraform
ARG TERRAFORM_VERSION=0.12.16
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/local/bin && \
    rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# install starship
RUN wget https://github.com/starship/starship/releases/download/v0.22.0/starship-x86_64-unknown-linux-musl.tar.gz && \
    tar -xzf starship-x86_64-unknown-linux-musl.tar.gz && \
    mv starship /usr/local/bin/ && \
    rm starship-x86_64-unknown-linux-musl.tar.gz

WORKDIR /workspace/infrastructure

# https://code.visualstudio.com/docs/remote/containers-advanced#_avoiding-extension-reinstalls-on-container-rebuild
RUN mkdir -p $HOME/.vscode-server
