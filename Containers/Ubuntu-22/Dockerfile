#
#  Dockerfile for building/testing Project MU with GCC.
#
#  Copyright (c) Microsoft Corporation
#  SPDX-License-Identifier: BSD-2-Clause-Patent
#

#
# The build container layer is intended for pipeline use and is the minimal set
# of tools required for building Project MU.
#
FROM ubuntu:22.04 AS build

# Versions
ARG GCC_MAJOR_VERSION=12
ARG NASM_VERSION=2.16.01
ARG IASL_VERSION=20210105
ARG CSPELL_VERSION=5.20.0
ARG MARKDOWNLINT_VERSION=0.31.0

# Set environment variable to avoid interaction.
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
        bison \
        ca-certificates \
        flex \
        git \
        lcov \
        m4 \
        make \
        mono-complete \
        nasm \
        npm \
        python3 \
        python3-pip \
        python3-venv \
        software-properties-common \
        sudo \
        uuid-dev \
        wget \
        && \
    apt-get install --yes --no-install-recommends \
        g++-${GCC_MAJOR_VERSION} gcc-${GCC_MAJOR_VERSION} \
        gcc-${GCC_MAJOR_VERSION}-x86-64-linux-gnux32 \
        gcc-${GCC_MAJOR_VERSION}-aarch64-linux-gnu \
        gcc-${GCC_MAJOR_VERSION}-riscv64-linux-gnu \
        gcc-${GCC_MAJOR_VERSION}-arm-linux-gnueabi \
        gcc-${GCC_MAJOR_VERSION}-arm-linux-gnueabihf \
        && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV GCC5_AARCH64_PREFIX /usr/bin/aarch64-linux-gnu-
ENV GCC5_ARM_PREFIX     /usr/bin/arm-linux-gnueabi-
ENV GCC5_RISCV64_PREFIX /usr/bin/riscv64-linux-gnu-

RUN pip install pip lcov_cobertura --upgrade

# RUN npm install -g npm
RUN npm install -g \
        cspell@${CSPELL_VERSION} \
        markdownlint-cli@${MARKDOWNLINT_VERSION}

RUN wget -O - https://www.nasm.us/pub/nasm/releasebuilds/${NASM_VERSION}/nasm-${NASM_VERSION}.tar.gz | \
    tar xz && cd nasm-${NASM_VERSION} && \
    ./autogen.sh && ./configure && make -j $(nproc) && make install && \
    cd .. && rm -rf nasm-${NASM_VERSION}

RUN wget -O - https://acpica.org/sites/acpica/files/acpica-unix-${IASL_VERSION}.tar.gz | \
    tar xz && cd acpica-unix-${IASL_VERSION} && \
    make clean && make -j $(nproc) iasl && make install && \
    cd .. && rm -rf acpica-unix-${IASL_VERSION}

RUN wget -q "https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb" && \
    dpkg -i packages-microsoft-prod.deb && rm packages-microsoft-prod.deb && \
    apt-get update && apt-get install -y powershell && apt-get clean

#
# Alternatives
#

RUN update-alternatives \
      --install /usr/bin/python python /usr/bin/python3.10 1 && \
    update-alternatives \
      --install /usr/bin/python3 python3 /usr/bin/python3.10 1 && \
    update-alternatives \
      --install /usr/bin/gcc gcc /usr/bin/gcc-${GCC_MAJOR_VERSION} 100 \
      --slave /usr/bin/g++ g++ /usr/bin/g++-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/gcc-ar gcc-ar /usr/bin/gcc-ar-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/gcc-nm gcc-nm /usr/bin/gcc-nm-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/gcc-ranlib gcc-ranlib /usr/bin/gcc-ranlib-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/gcov gcov /usr/bin/gcov-${GCC_MAJOR_VERSION} && \
    update-alternatives \
      --install /usr/bin/cpp cpp /usr/bin/cpp-${GCC_MAJOR_VERSION} 100 && \
    update-alternatives \
      --install /usr/bin/aarch64-linux-gnu-gcc aarch64-linux-gnu-gcc /usr/bin/aarch64-linux-gnu-gcc-${GCC_MAJOR_VERSION} 100 \
      --slave /usr/bin/aarch64-linux-gnu-g++ aarch64-linux-gnu-g++ /usr/bin/aarch64-linux-gnu-g++-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/aarch64-linux-gnu-gcc-ar aarch64-linux-gnu-gcc-ar /usr/bin/aarch64-linux-gnu-gcc-ar-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/aarch64-linux-gnu-gcc-nm aarch64-linux-gnu-gcc-nm /usr/bin/aarch64-linux-gnu-gcc-nm-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/aarch64-linux-gnu-gcc-ranlib aarch64-linux-gnu-gcc-ranlib /usr/bin/aarch64-linux-gnu-gcc-ranlib-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/aarch64-linux-gnu-gcov aarch64-linux-gnu-gcov /usr/bin/aarch64-linux-gnu-gcov-${GCC_MAJOR_VERSION} && \
    update-alternatives \
      --install /usr/bin/arm-linux-gnueabi-gcc arm-linux-gnueabi-gcc /usr/bin/arm-linux-gnueabi-gcc-${GCC_MAJOR_VERSION} 100 \
      --slave /usr/bin/arm-linux-gnueabi-g++ arm-linux-gnueabi-g++ /usr/bin/arm-linux-gnueabi-g++-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/arm-linux-gnueabi-gcc-ar arm-linux-gnueabi-gcc-ar /usr/bin/arm-linux-gnueabi-gcc-ar-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/arm-linux-gnueabi-gcc-nm arm-linux-gnueabi-gcc-nm /usr/bin/arm-linux-gnueabi-gcc-nm-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/arm-linux-gnueabi-gcc-ranlib arm-linux-gnueabi-gcc-ranlib /usr/bin/arm-linux-gnueabi-gcc-ranlib-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/arm-linux-gnueabi-gcov arm-linux-gnueabi-gcov /usr/bin/arm-linux-gnueabi-gcov-${GCC_MAJOR_VERSION} && \
    update-alternatives \
      --install /usr/bin/riscv64-linux-gnu-gcc riscv64-linux-gnu-gcc /usr/bin/riscv64-linux-gnu-gcc-${GCC_MAJOR_VERSION} 100 \
      --slave /usr/bin/riscv64-linux-gnu-g++ riscv64-linux-gnu-g++ /usr/bin/riscv64-linux-gnu-g++-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/riscv64-linux-gnu-gcc-ar riscv64-linux-gnu-gcc-ar /usr/bin/riscv64-linux-gnu-gcc-ar-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/riscv64-linux-gnu-gcc-nm riscv64-linux-gnu-gcc-nm /usr/bin/riscv64-linux-gnu-gcc-nm-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/riscv64-linux-gnu-gcc-ranlib riscv64-linux-gnu-gcc-ranlib /usr/bin/riscv64-linux-gnu-gcc-ranlib-${GCC_MAJOR_VERSION} \
      --slave /usr/bin/riscv64-linux-gnu-gcov riscv64-linux-gnu-gcov /usr/bin/riscv64-linux-gnu-gcov-${GCC_MAJOR_VERSION}

#
# The test container layer is intended for pipeline use and virtual platform tools
# on top of the base build image.
#
FROM build AS test

ARG QEMU_URL="https://gitlab.com/qemu-project/qemu.git"
ARG QEMU_BRANCH="v8.0.0"

RUN apt-get update && apt-get install --yes --no-install-recommends \
        autoconf \
        automake \
        autotools-dev \
        bc \
        build-essential \
        curl \
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
    git clone "${QEMU_URL}" --branch "${QEMU_BRANCH}" --depth 1 qemu && \
    cd qemu && \
    ./configure --target-list=x86_64-softmmu,aarch64-softmmu --enable-gtk && \
    make install -j $(nproc) && \
    cd .. && \
    rm -rf qemu && \
    apt remove --yes ninja-build && \
    apt-get clean

#
# The dev container layer is intended for local use and has more robust tooling
# and environment configurations for developers.
#
FROM test AS dev

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
        nano \
        less \
        && \
    apt-get clean
