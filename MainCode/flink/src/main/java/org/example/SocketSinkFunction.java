package org.example;

import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.sink.RichSinkFunction;

import java.io.DataOutputStream;
import java.io.OutputStream;
import java.net.Socket;

public class SocketSinkFunction extends RichSinkFunction<String> {

    Socket socket;

    @Override
    public void open(Configuration parameters) throws Exception {
        super.open(parameters);
        socket = new Socket("localhost", 9999);
    }

    @Override
    public void invoke(String value, Context context) throws Exception {
        super.invoke(value, context);
        OutputStream outputStream = socket.getOutputStream();
        DataOutputStream out = new DataOutputStream(outputStream);
        out.writeUTF(value);
    }

    @Override
    public void close() throws Exception {
        super.close();
        socket.close();
    }
}
