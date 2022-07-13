# Confluent 10x Storage Demo

Work in progress

## Introduction to Confluent and Intelligent Storage

Confluent is the world leader for Data in Motion. Confluent Cloud is our fully managed, cloud-native service for connecting and processing all of your data, everywhere it’s needed. To build Confluent Cloud, we rearchitected Apache Kafka® to make a service that's [10x better](https://www.confluent.io/blog/making-apache-kafka-service-10x-better/?utm_campaign=tm.campaigns_cd.making-confluent-cloud-10x-more-elastic-than-apache-kafka&utm_medium=blogpost).

**Confluent Infinite Storage** allows you to store data in your Kafka cluster indefinitely, opening up new use cases and simplifying your architecture. Instead of moving data *through* Kafka from sources to sinks, you could instead *keep* the data in Kafka indefinitely and re-read it when you need it, using exactly the same stream processing APIs you use for real-time applications (so-called [Kappa Architecture](https://www.oreilly.com/radar/questioning-the-lambda-architecture/)).

You can learn more about how Confluent is able to provide infinite storage retention from the [Tiered Storage lesson](https://developer.confluent.io/learn-kafka/architecture/tiered-storage/?utm_campaign=tm.campaigns_cd.making-confluent-cloud-10x-more-elastic-than-apache-kafka&utm_medium=blogpost) in the free Kafka Internals course authored by Dave Shook and Kafka inventor Jun Rao.

## This Demo -- Machine Learning Model Training

Machine learning provides an ideal demonstration of Confluent Infinite Storage.
Kafka has long been instrumental for *deploying* models to make real-time predictions, but when it comes to *training* models, Kafka is often only used as a "dumb pipe" to get data into a long term storage system like S3, Google Cloud Storage, Azure Blob Storage, HDFS etc. That's because Kafka generally only retains data for 7 days -- it's not built as a long term storage service.

Confluent Infinite Storage changes that. Now, your Kafka cluster is the data lake. Storing training data in a Kafka topic indefinitely has several benefits, including:
- No need to send data to a separate data lake like S3, GCS, HDFS, etc., thus simplifying your architecture
- One data pipeline for 
  - data preprocessing
  - model training
  - real-time predictions
  - real-time and historical model performance monitoring
  - replaying historical events
- Both new and historical events are available for other stream processing applications to take advantage of

This demo is derived from the offical TensorFlow Kafka tutorial: [Robust machine learning on streaming data using Kafka and Tensorflow-IO](https://www.tensorflow.org/io/tutorials/kafka). It is based on the [SUSY](https://archive.ics.uci.edu/ml/datasets/SUSY#) dataset, which is data about high energy particles gathered from the Large Hadron Collider. The goal of the machine learning model is to distinguish between a "signal process" (value of 1) and a "background process" (value of 0).

> Aside: In this context, "signal" means supersymmetric particles were produced, and "background" means no supersymmetry was observed.

## Instructions

### Setup Confluent Cloud
1. Sign up for a Confluent Cloud Account.

1. In the Confluent Cloud console, create a basic cluster called "10x Demo" in the cloud region of your choice.

1. Create a topic for the training data. Go to Topics -> Add topic -> advanced settings
    - Set topic name to `10x.storage.machine-learning.train`
    - Set retention time to `infinite`
    - Select "Save & create"

1. Create a topic for the validation data. Go to Topics -> Add topic -> advanced settings
    - Set topic name to `10x.storage.machine-learning.test`
    - Set retention time to `infinite`    
    - Select "Save & create"

1. Create an API key for your cluster. Go to Data integration -> API keys -> Add key and choose global access. Keep this API key secure with a password manager.

1. In your Confluent Cloud environment, select **Schema Registry** and enable Confluent Schema Registry in the same region as your cluster.

1. Create an API key for your Schema Registry. Go to the Schema Registry tab in your Confluent Cloud environment, select "API credentials" and create a new API key. Keep this API key secure with a password manager.

### Setup Your Workstation

1. Clone this repository and change into the directory.
    ```
    git clone https://github.com/confluentinc/demo-10x-storage.git
    cd demo-10x-storage
    ```

1. In this project folder a file called `.env` with these variables defined to match your environment.
    ```
    CCLOUD_BOOTSTRAP_ENDPOINT=
    CCLOUD_CLUSTER_API_KEY=
    CCLOUD_CLUSTER_API_SECRET=
    CCLOUD_SCHEMA_REGISTRY_ENDPOINT=
    CCLOUD_SCHEMA_REGISTRY_API_KEY=
    CCLOUD_SCHEMA_REGISTRY_API_SECRET=
    ```
    You can get the Schema Registry endpoint by logging in to the Confluent Cloud Console and navigating Environments -> {your environment} -> Schema Registry and then scroll down to "API Endpoint".
    You can get the bootstrap endpoint from Environments -> {your environment} -> {your cluster} -> Cluster overview -> Cluster settings in the Confluent Cloud Console.

1. Create a python virtual environment called `.venv` and install dependencies.
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

1. Download and uncompress the SUSY dataset (~2GB uncompressed).
    ```
    curl -sSOL https://archive.ics.uci.edu/ml/machine-learning-databases/00279/SUSY.csv.gz
    gunzip SUSY.csv.gz
    ```



## Note about Online Machine Learning

Online Machine Learning ([wikpedia](https://en.wikipedia.org/wiki/Online_machine_learning)) refers to a method of model training where the model incrementally improves with new data, as opposed to requiring the entire dataset be processed in batch. Online learning is a perfect fit for Apache Kafka because a model can subscribe to a topic and continuously train as more data arrives, periodically checkpointing its current state to an external repository to be used to make predications. The [`tfio.experimental.streaming.KafkaBatchIODataset`](https://www.tensorflow.org/io/api_docs/python/tfio/experimental/streaming/KafkaBatchIODataset) class is an example of an API that can employ Online Machine Learning.

The downside to Online Machine Learning is it is only available to a small subset of algorithms, which may not be ideal or even applicable to certain use cases.

## Further Reading

### Python:  Code Example for Apache Kafka®

Full code example for creating Kafka client applications in Python:
- [https://docs.confluent.io/platform/current/tutorials/examples/clients/docs/python.html](https://docs.confluent.io/platform/current/tutorials/examples/clients/docs/python.html?utm_source=github&utm_medium=demo&utm_campaign=ch.examples_type.community_content.clients-ccloud)

### ksqlDB Recipe -- Retrain a Machine Learning Model

- https://developer.confluent.io/tutorials/model-retraining/confluent.html
- Associated [blog post](https://www.confluent.io/blog/how-baader-built-a-predictive-analytics-machine-learning-system-with-kafka-and-rstudio/)
### Streaming Machine Learning at Scale from 100000 IoT Devices with HiveMQ, Apache Kafka and TensorFLow

This is an in-depth, end-to-end demo on Google Cloud Platform that shows machine learning model training and real-time predictions for high volume Internet of Things (IoT) data (specifically car sensors).

- https://github.com/kaiwaehner/hivemq-mqtt-tensorflow-kafka-realtime-iot-machine-learning-training-inference
- Associated [blog post](https://www.confluent.io/blog/streaming-machine-learning-with-tiered-storage/)