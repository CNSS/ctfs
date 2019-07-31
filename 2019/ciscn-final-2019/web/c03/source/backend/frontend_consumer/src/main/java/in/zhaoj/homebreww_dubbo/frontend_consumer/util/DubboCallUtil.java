package in.zhaoj.homebreww_dubbo.frontend_consumer.util;

import com.fasterxml.jackson.core.JsonProcessingException;
import in.zhaoj.homebreww_dubbo.frontend_consumer.compoment.ServiceComponent;
import in.zhaoj.homebreww_dubbo.frontend_consumer.pojo.Node;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.integration.ip.tcp.serializer.ByteArrayCrLfSerializer;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.util.HashMap;

/**
 * @author: ciscn
 * @date:2019-07-03
 * @description:
 */
@Component
public class DubboCallUtil {

    @Autowired
    private ServiceComponent serviceComponent;

    @Autowired
    private JSONUtil jsonUtil;

    public HashMap<String, Object> getAllNodes() {
        return serviceComponent.getNodesHashMap();
    }

    public HashMap<String, Object> callWithRetry(String serviceName, String methodName, HashMap<String, Object> hashMap) {
        for(int i = 0; i < 5; i++) {
            HashMap<String, Object> returnHashMap = call(serviceName, methodName, hashMap);
            if(returnHashMap != null) {
                return returnHashMap;
            }
        }

        return null;
    }

    public HashMap<String, Object> call(String serviceName, String methodName, HashMap<String, Object> hashMap) {
        Node node = this.serviceComponent.getNodeForService(serviceName);

        HashMap<String, Object> callHashMap = new HashMap<>();
        callHashMap.put("opt", "call");
        callHashMap.put("method", methodName);
        callHashMap.put("parameter", hashMap);
        String sendJson;
        try {
            sendJson = this.jsonUtil.encode(callHashMap);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
            return null;
        }

        String returnMessage = "";

        Socket clientSocket = null;
        OutputStream outputStream = null;
        InputStream inputStream = null;
        try {
            String sentence;
            clientSocket = new Socket(node.getIp(), node.getPort());
            clientSocket.setSoTimeout(5000);
            sentence = sendJson;

            ByteArrayCrLfSerializer byteArrayCrLfSerializer = new ByteArrayCrLfSerializer();
            byteArrayCrLfSerializer.setMaxMessageSize(15 * 1024 * 1024);
            outputStream = clientSocket.getOutputStream();
            byteArrayCrLfSerializer.serialize(sentence.getBytes(), outputStream);

            inputStream = clientSocket.getInputStream();
            returnMessage = new String(byteArrayCrLfSerializer.deserialize(inputStream));

        } catch (Exception e) {
            e.printStackTrace();
            return null;
        } finally {
            try {
                outputStream.close();
                inputStream.close();
                clientSocket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        try {
            if(returnMessage.substring(0, 1).equals(" ")) {
                returnMessage = returnMessage.substring(1);
            }

            return (HashMap<String, Object>) jsonUtil.decode(returnMessage).getOrDefault("data", new HashMap<String, Object>());
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }
}
