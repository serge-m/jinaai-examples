FROM pytorch/pytorch:latest

WORKDIR /

RUN apt-get update && \
    apt-get install --no-install-recommends -y curl libmagic-dev

RUN python -m pip install --no-cache-dir click \
                               jina[http]==0.4.1 \
                               jina[devel]==0.4.1 \
                               pillow \
                               docker \
                               uvloop

RUN python -c "import torchvision.models as models; models.mobilenet_v2(pretrained=True)"


ENV ENCODER yaml/encode.yml
ENV TMP_WORKSPACE data/workspace

COPY app.py flow-index.yml flow-query.yml /
COPY yaml /yaml


CMD ["python", "app.py","-t","query"]
