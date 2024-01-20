# LlamaCppDocker

This project contains two main components

- A Dockerized image with LlamaCppPython with CUDA support
- A Dockerized image built on the previous one with a simple python application that uses **Mistral 7B** to extract information from a series of Job Ads. (#OpenToWork)

My machine is Windows 11 with an RTX 3070, NVidia drivers 546.12, CUDA 12.3 ([CUDA Toolkit download](https://developer.nvidia.com/cuda-downloads))

# Instructions

1. Clone the repo
2. Build the base image with llama-cpp-python with CUDA support
3. Build the app image
4. Use you own python app and have fun 🎉

## Base image

To speed up the development process we will build a base image with CUDA and llama-cpp-python.

If you have other requirements in your project put them inside this image, it will make building and iterating on your app image much faster.

From the root folder of the project run

```powershell
docker build --build-arg GPU_ENABLED=true -t llama-cpp-python-docker:12.1.1 -f .\docker\llama-cpp-python-docker\Dockerfile .
```

## App Image

I used `dolphin-2.6-mistral-7b.Q5_0.gguf` but feel free to use any model you like.

Mistral models can be downloaded from [TheBloke@HuggingFace](https://huggingface.co/TheBloke/dolphin-2.6-mistral-7B-GGUF).

Note: it is possible to not use a volume and map a local folder but the performace hit is enormous. I **strongly** encourage to use the volume approach.

### Create a volume.

```
docker volume create gguf_models
```

This command will use "dummy" docker image to copy the model into the volume.

Copy the Mistral model into the volume by running the following command:

```
docker run --rm -v gguf_models:/vol -v C:\lmstudio\models\TheBloke\dolphin-2.6-mistral-7B-GGUF:/src alpine cp /src/dolphin-2.6-mistral-7b.Q5_0.gguf /vol/
```

### Build and run the app image

```
docker build --build-arg GPU_ENABLED=true -f docker/test-app/Dockerfile -t test_app .

docker run -d --gpus=all --cap-add SYS_RESOURCE -e USE_MLOCK=0 -e MODEL=/var/model/dolphin-2.6-mistral-7b.Q5_0.gguf -v gguf_models:/var/model -p 8000:8000 -t test_app
```

Inspect the output of the container logs from Docker Desktop to see the result.