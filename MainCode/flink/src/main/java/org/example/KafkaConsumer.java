package org.example;

import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer010;

import java.util.Properties;

public class KafkaConsumer {
    public static void main(String[] args) {
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setParallelism(2);
        Properties properties = new Properties();
        properties.setProperty("bootstrap.servers", "localhost:9093,localhost:9092,localhost:9094");
        DataStream<String> stream = env
                .addSource(new FlinkKafkaConsumer010<>("flink-stream-in-topic", new SimpleStringSchema(), properties));
        stream.writeToSocket("127.0.0.1", 9999, new SimpleStringSchema());
//        stream.addSink(new SocketSinkFunction());
        try {
            env.execute("Flink Streaming");
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
