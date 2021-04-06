FROM public.ecr.aws/lambda/python:3.8

# install build libs
RUN yum groupinstall -y "Development Tools" \
    && yum install -y which openssl \
    && yum install -y sudo

# install mecab, ipadic, ipadic-neologd
WORKDIR /tmp
RUN  curl -L "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE" -o mecab-0.996.tar.gz \
    && tar xzf mecab-0.996.tar.gz \
    && cd mecab-0.996 \
    && ./configure \
    && make \
    && make check \
    && make install \
    && cd .. \
    && rm -rf mecab-0.996*

WORKDIR /tmp
RUN curl -L "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7MWVlSDBCSXZMTXM" -o mecab-ipadic-2.7.0-20070801.tar.gz \
    && tar -zxvf mecab-ipadic-2.7.0-20070801.tar.gz \
    && cd mecab-ipadic-2.7.0-20070801 \
    && ./configure --with-charset=utf8 \
    && make \
    && make install \
    && cd .. \
    && rm -rf mecab-ipadic-2.7.0-20070801

WORKDIR /tmp
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
    && cd mecab-ipadic-neologd \
    && ./bin/install-mecab-ipadic-neologd -n -a -y -p /var/lib/mecab/dic/mecab-ipadic-neologd \
    && rm -rf mecab-ipadic-neologd
RUN mkdir -p /usr/lib/mecab && ln -s /var/lib/mecab/dic /usr/lib/mecab/dic

WORKDIR /var/task
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pip install pipenv
RUN pipenv install --system

# set function code
COPY src ./src/
COPY lambda_handler.py ./
ARG FUNCTION_DIR="/var/task/"
ENV CONFIG_PATH="/var/task/src/config.yaml"
CMD ["lambda_handler.lambda_handler"]
