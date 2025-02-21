#
#  Dockerfile for building/testing Project MU with GCC.
#
# NOTE: This file is automatically synchronized from Mu DevOps. Update the original file there
#       instead of the file in this repo.
#
# - Mu DevOps Repo: https://github.com/microsoft/mu_devops
# - File Sync Settings: https://github.com/microsoft/mu_devops/blob/main/.sync/Files.yml
#
#  Copyright (c) Microsoft Corporation
#  SPDX-License-Identifier: BSD-2-Clause-Patent
#

{% import '../../Version.njk' as sync_version -%}

{% raw %}
# NOTE: Because this pipeline YAML file is a Nunjucks template, the pipeline syntax of `{{}}` will conflict with
#       Nunjucks style. Surround pipeline YAML code that uses `{{}}` within `raw` and `endraw` tags
#       to allow it to pass through Nunjucks processing.

#
# The build container layer is intended for pipeline use and is the minimal set
# of tools required for building Project MU.
#
FROM ubuntu:22.04 AS build

# Versions
# Visit this NuGet package version page to see the latest version available
# https://dev.azure.com/projectmu/acpica/_artifacts/feed/mu_iasl/NuGet/edk2-acpica-iasl/versions
ARG GCC_MAJOR_VERSION=12 \
    NASM_VERSION=2.16.01 \
    CSPELL_VERSION=5.20.0 \
    MARKDOWNLINT_VERSION=0.32.2 \
    IASL_VERSION=20210105.0.6

# Work-around for azure pipelines adding the vsts_azpcontainer user, but not adding
# the .local/bin directory to the path which will be used by pip.
# Set environment variable to avoid interaction.
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=UTC \
    PATH=$PATH:/home/vsts_azpcontainer/.local/bin

RUN echo "Installing needed system packages" \
    && apt-get update \
    && apt-get install --yes --no-install-recommends \
        bison \
        ca-certificates \
        curl \
        flex \
        git \
        gnupg \
        gnupg2 \
        lcov \
        jq \
        m4 \
        make \
        mono-complete \
        nasm \
        npm \
        software-properties-common \
        sudo \
        unzip \
        uuid-dev \
        wget && \
    echo "\n\n Adding keys, repos" \
    && apt-get update \
    && apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys F23C5A6CF475977595C89F51BA6932366A755776 \
    && add-apt-repository ppa:deadsnakes/ppa -y && \

    echo "\n\n Installing python/gcc" \
    && apt-get update \
    && apt-get install --yes --no-install-recommends \
        {% endraw %}python{{ sync_version.python_version }}{% raw %} \
        {% endraw %}python{{ sync_version.python_version }}{% raw %}-venv \
        g++-${GCC_MAJOR_VERSION} gcc-${GCC_MAJOR_VERSION} \
        gcc-${GCC_MAJOR_VERSION}-x86-64-linux-gnux32 \
        gcc-${GCC_MAJOR_VERSION}-aarch64-linux-gnu \
        gcc-${GCC_MAJOR_VERSION}-riscv64-linux-gnu \
        gcc-${GCC_MAJOR_VERSION}-arm-linux-gnueabi \
        gcc-${GCC_MAJOR_VERSION}-arm-linux-gnueabihf \
    && curl -O https://bootstrap.pypa.io/get-pip.py \
    && {% endraw %}python{{ sync_version.python_version }}{% raw %} get-pip.py \
    && {% endraw %}python{{ sync_version.python_version }}{% raw %} -m pip install --upgrade setuptools \
    && rm get-pip.py \
    && apt-get upgrade -y && \

    echo "\n\n Cleaning cache" \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV GCC5_AARCH64_PREFIX /usr/bin/aarch64-linux-gnu- \
    GCC5_ARM_PREFIX     /usr/bin/arm-linux-gnueabi- \
    GCC5_RISCV64_PREFIX /usr/bin/riscv64-linux-gnu-

RUN echo "Upgrading pip/lcov_cobertura" \
    && pip install pip lcov_cobertura --upgrade && \

    echo "\n\n npm packages" \
    && npm install -g \
        cspell@${CSPELL_VERSION} \
        markdownlint-cli@${MARKDOWNLINT_VERSION} && \

    echo "\n\n Building nasm" \
    && wget -O - https://www.nasm.us/pub/nasm/releasebuilds/${NASM_VERSION}/nasm-${NASM_VERSION}.tar.gz | tar xz \
    && cd nasm-${NASM_VERSION} \
    && ./autogen.sh \
    && ./configure \
    && make -j $(nproc) \
    && make install \
    && cd .. \
    && rm -rf nasm-${NASM_VERSION} && \

    echo "\n\n Iasl_temp" \
    && mkdir -p iasl_temp \
    && cd iasl_temp \
    && wget -O iasl_${IASL_VERSION}.nupkg "https://pkgs.dev.azure.com/projectmu/acpica/_apis/packaging/feeds/mu_iasl/nuget/packages/edk2-acpica-iasl/versions/${IASL_VERSION}/content?api-version=6.0-preview.1" \
    && unzip iasl_${IASL_VERSION}.nupkg -d /iasl_pkg_contents \
    && cp /iasl_pkg_contents/edk2-acpica-iasl/Linux-x86/iasl /usr/bin/iasl && chmod +x /usr/bin/iasl \
    && chmod +x /usr/bin/iasl \
    && cd .. \
    && rm -rf iasl_temp && \

    echo "\n\n Installing powershell" \
    && wget -q "https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb" \
    && dpkg -i packages-microsoft-prod.deb \
    && rm packages-microsoft-prod.deb \
    && apt-get update \
    && apt-get install -y powershell && \

    echo "\n\n Cleaning cache" \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#
# Rust support
#

ENV CARGO_HOME="$HOME/.cargo" \
    RUSTUP_HOME="$HOME/.rustup" \
    PATH="$CARGO_HOME/bin:$PATH"

# Install Rust/Cargo and extras (rust-src, rust fmt, cargo-make, cargo-tarpaulin)
RUN echo "Installing Rust/Cargo and extras (rust-src, rust fmt)" \
    && VERSION_URL="https://raw.githubusercontent.com/microsoft/mu_devops/main/.sync/Version.njk" \
    && RUST_VERSION=$(curl -s ${VERSION_URL} | grep -oP '(?<=rust_toolchain = ").*(?=")') \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain ${RUST_VERSION} --profile minimal \
    && . /.cargo/env \
    && rustup component add rustfmt rust-src --toolchain ${RUST_VERSION}-x86_64-unknown-linux-gnu && \

    echo "\n\n Installing cargo-make, cargo-tarpaulin" \
    && mkdir cargo_downloads \
    && cd cargo_downloads \
    && TAG_NAME=$(curl -s https://api.github.com/repos/sagiegurari/cargo-make/releases/latest | jq -r '.tag_name') \
    && DOWNLOAD_URL="https://github.com/sagiegurari/cargo-make/releases/download/$TAG_NAME/cargo-make-v$TAG_NAME-x86_64-unknown-linux-gnu.zip" \
    && curl -L -o cargo-make.zip "$DOWNLOAD_URL" \
    && unzip cargo-make.zip \
    && mv cargo-make-v$TAG_NAME-x86_64-unknown-linux-gnu/cargo-make $CARGO_HOME/bin/ \
    && TAG_NAME=$(curl -s https://api.github.com/repos/xd009642/tarpaulin/releases/latest | jq -r '.tag_name') \
    && DOWNLOAD_URL="https://github.com/xd009642/tarpaulin/releases/download/$TAG_NAME/cargo-tarpaulin-x86_64-unknown-linux-gnu.tar.gz" \
    && curl -L -o cargo-tarpaulin.tar.gz "$DOWNLOAD_URL" \
    && tar -xzvf cargo-tarpaulin.tar.gz \
    && mv cargo-tarpaulin $CARGO_HOME/bin/ \
    && cd .. \
    && rm -r cargo_downloads

#
# Alternatives
#
{% endraw %}

RUN update-alternatives \
      --install /usr/bin/python python /usr/bin/python{{ sync_version.python_version }} 1 \
    && update-alternatives \
      --install /usr/bin/python3 python3 /usr/bin/python{{ sync_version.python_version }} 1 \
    && update-alternatives \
      --install /usr/bin/gcc gcc /usr/bin/gcc-${GCC_MAJOR_VERSION} 100 \
      --slave /usr/bin/g++ g++ /usr/bin/g++-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/gcc-ar gcc-ar /usr/bin/gcc-ar-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/gcc-nm gcc-nm /usr/bin/gcc-nm-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/gcc-ranlib gcc-ranlib /usr/bin/gcc-ranlib-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/gcov gcov /usr/bin/gcov-${GCC_MAJOR_VERSION} \
    && update-alternatives \
      --install /usr/bin/cpp cpp /usr/bin/cpp-${GCC_MAJOR_VERSION} 100 \
    && update-alternatives \
      --install /usr/bin/aarch64-linux-gnu-gcc aarch64-linux-gnu-gcc /usr/bin/aarch64-linux-gnu-gcc-${GCC_MAJOR_VERSION} 100 \
      --slave /usr/bin/aarch64-linux-gnu-cpp aarch64-linux-gnu-cpp /usr/bin/aarch64-linux-gnu-cpp-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/aarch64-linux-gnu-g++ aarch64-linux-gnu-g++ /usr/bin/aarch64-linux-gnu-g++-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/aarch64-linux-gnu-gcc-ar aarch64-linux-gnu-gcc-ar /usr/bin/aarch64-linux-gnu-gcc-ar-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/aarch64-linux-gnu-gcc-nm aarch64-linux-gnu-gcc-nm /usr/bin/aarch64-linux-gnu-gcc-nm-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/aarch64-linux-gnu-gcc-ranlib aarch64-linux-gnu-gcc-ranlib /usr/bin/aarch64-linux-gnu-gcc-ranlib-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/aarch64-linux-gnu-gcov aarch64-linux-gnu-gcov /usr/bin/aarch64-linux-gnu-gcov-${GCC_MAJOR_VERSION} \
    && update-alternatives \
      --install /usr/bin/arm-linux-gnueabi-gcc arm-linux-gnueabi-gcc /usr/bin/arm-linux-gnueabi-gcc-${GCC_MAJOR_VERSION} 100 \
      --slave /usr/bin/arm-linux-gnueabi-cpp arm-linux-gnueabi-cpp /usr/bin/arm-linux-gnueabi-cpp-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/arm-linux-gnueabi-g++ arm-linux-gnueabi-g++ /usr/bin/arm-linux-gnueabi-g++-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/arm-linux-gnueabi-gcc-ar arm-linux-gnueabi-gcc-ar /usr/bin/arm-linux-gnueabi-gcc-ar-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/arm-linux-gnueabi-gcc-nm arm-linux-gnueabi-gcc-nm /usr/bin/arm-linux-gnueabi-gcc-nm-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/arm-linux-gnueabi-gcc-ranlib arm-linux-gnueabi-gcc-ranlib /usr/bin/arm-linux-gnueabi-gcc-ranlib-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/arm-linux-gnueabi-gcov arm-linux-gnueabi-gcov /usr/bin/arm-linux-gnueabi-gcov-${GCC_MAJOR_VERSION} \
    && update-alternatives \
      --install /usr/bin/riscv64-linux-gnu-gcc riscv64-linux-gnu-gcc /usr/bin/riscv64-linux-gnu-gcc-${GCC_MAJOR_VERSION} 100 \
      --slave /usr/bin/riscv64-linux-gnu-cpp riscv64-linux-gnu-cpp /usr/bin/riscv64-linux-gnu-cpp-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/riscv64-linux-gnu-g++ riscv64-linux-gnu-g++ /usr/bin/riscv64-linux-gnu-g++-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/riscv64-linux-gnu-gcc-ar riscv64-linux-gnu-gcc-ar /usr/bin/riscv64-linux-gnu-gcc-ar-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/riscv64-linux-gnu-gcc-nm riscv64-linux-gnu-gcc-nm /usr/bin/riscv64-linux-gnu-gcc-nm-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/riscv64-linux-gnu-gcc-ranlib riscv64-linux-gnu-gcc-ranlib /usr/bin/riscv64-linux-gnu-gcc-ranlib-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/riscv64-linux-gnu-gcov riscv64-linux-gnu-gcov /usr/bin/riscv64-linux-gnu-gcov-${GCC_MAJOR_VERSION} && \

      echo "\n\n\n Cleaning cache" \
      && apt-get autoremove \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*

{% raw %}
#
# The test container layer is intended for pipeline use and virtual platform tools
# on top of the base build image.
#
FROM build AS test

ARG QEMU_URL="https://gitlab.com/qemu-project/qemu.git" \
    QEMU_BRANCH="v9.0.0"

RUN echo "Installing needed software to build qemu." \
    && apt-get update \
    && apt-get install --yes --no-install-recommends \
        autoconf \
        automake \
        autotools-dev \
        bc \
        build-essential \
        dosfstools \
        gcc \
        libglib2.0-dev \
        libgtk-3-dev \
        libpixman-1-dev \
        libsdl2-dev \
        mtools \
        ninja-build \
        tar \
        && \

    echo "\n\n Installing/Building qemu" \
    && git clone "${QEMU_URL}" --branch "${QEMU_BRANCH}" --depth 1 qemu \
    && cd qemu \
    && ./configure --target-list=x86_64-softmmu,aarch64-softmmu --enable-gtk \
    && make install -j $(nproc) \
    && cd .. \
    && rm -rf qemu \
    && apt-get remove --yes ninja-build && \

    echo "\n\n Cleaning cache" \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#
# The dev container layer is intended for local use and has more robust tooling
# and environment configurations for developers.
#
FROM test AS dev

RUN echo "Installing nano/less" \
    && apt-get update \
    && apt-get install --yes --no-install-recommends \
        nano \
        less \
        && \

    echo "\n\n Cleaning cache" \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

{% endraw %}
