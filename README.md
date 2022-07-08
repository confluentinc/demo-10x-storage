# Confluent 10x Storage Demo

Work in progress

## Introduction to Confluent and Intelligent Storage

Confluent is the world leader for Data in Motion. Confluent Cloud is our fully managed, cloud-native service for connecting and processing all of your data, everywhere it’s needed. To build Confluent Cloud, we rearchitected Apache® Kafka to make a service that's [10x better](https://www.confluent.io/blog/making-apache-kafka-service-10x-better/?utm_campaign=tm.campaigns_cd.making-confluent-cloud-10x-more-elastic-than-apache-kafka&utm_medium=blogpost).

**Confluent Intelligent Storage** (also known to as Infinite or Tiered storage) allows you to store data in your Kafka cluster indefinitely, opening up new use cases and simplifying your architecture. Instead of moving data *through* Kafka from sources to sinks, you could instead *keep* the data in Kafka indefinitely and re-read it when you need it. All your data flows through Kafka anyway, so why not keep it there

You can learn more about how Confluent is able to provide infinite storage retention from the [Tiered Storage lesson](https://developer.confluent.io/learn-kafka/architecture/tiered-storage/?utm_campaign=tm.campaigns_cd.making-confluent-cloud-10x-more-elastic-than-apache-kafka&utm_medium=blogpost) in the free Kafka Internals course authored by Dave Shook and Kafka inventor Jun Rao.

## This Demo -- Machine Learning Model Training

Machine learning provides an ideal demonstration of Confluent Intelligent Storage. Storing training data in Kafka indefinitely has several benefits, including:
- No need to send data to a sink system like Spark or S3, thus simplifying your architecture and saving on costs
- Train different ML algorithms on the same data in parallel to see which model works best
- 

This demo is derived from the offical TensorFlow Kafka tutorial: [Robust machine learning on streaming data using Kafka and Tensorflow-IO](https://www.tensorflow.org/io/tutorials/kafka). It is based on the [SUSY](https://archive.ics.uci.edu/ml/datasets/SUSY#) dataset, which is data about high energy particles gathered from the Large Hadron Collider.

## Instructions

### Setup
1. Sign up for a Confluent Cloud Account.

1. In the Confluent Cloud console, create a basic cluster and then create topics:
    - `10x.storage.machine-learning.train`
    - `10x.storage.machine-learning.test`

1. Create a file called `.env` with these variables defined to match your environment.
    ```
    CCLOUD_BOOTSTRAP_ENDPOINT=
    CCLOUD_CLUSTER_API_KEY=
    CCLOUD_CLUSTER_API_SECRET=
    ```
1.

```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Note about Online Machine Learning

Online Machine Learning ([wikpedia](https://en.wikipedia.org/wiki/Online_machine_learning)) refers to a method of model training where the model incrementally improves with new data, as opposed to requiring the entire dataset be processed in batch. Online learning is a perfect fit for Apache Kafka,

## Further Reading

### ksqlDB Recipe -- Retrain a Machine Learning Model

- https://developer.confluent.io/tutorials/model-retraining/confluent.html
- Associated [blog post](https://www.confluent.io/blog/how-baader-built-a-predictive-analytics-machine-learning-system-with-kafka-and-rstudio/)
### Streaming Machine Learning at Scale from 100000 IoT Devices with HiveMQ, Apache Kafka and TensorFLow
- https://github.com/kaiwaehner/hivemq-mqtt-tensorflow-kafka-realtime-iot-machine-learning-training-inference
- In-depth, end-to-end demo on Google Cloud Platform that shows machine learning model training and real-time inference for high volume Internet of Things (IoT) data (specifically car sensors)
- Associated [blog post](https://www.confluent.io/blog/streaming-machine-learning-with-tiered-storage/)

Awesome quote from Kai Waehner, Confluent Field CTO:
> [With Confluent Intelligent Storage]...you don't need another data store anymore! Just ingest the data directly from the distributed commit log of Kafka. [You can train] different models with the same data, allowing you to use different ML frameworks. This totally simplifies your architecture -- no additional data store like S3, HDFS, or Spark required!