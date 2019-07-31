package in.zhaoj.homebrew_dubbo.storage_provider.bean;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.integration.annotation.ServiceActivator;
import org.springframework.integration.annotation.Transformer;
import org.springframework.integration.channel.DirectChannel;
import org.springframework.integration.ip.tcp.TcpInboundGateway;
import org.springframework.integration.ip.tcp.connection.AbstractServerConnectionFactory;
import org.springframework.integration.ip.tcp.connection.TcpNioServerConnectionFactory;
import org.springframework.integration.ip.tcp.serializer.ByteArrayCrLfSerializer;
import org.springframework.messaging.MessageChannel;

import java.lang.reflect.Method;
import java.util.HashMap;
import java.util.Map;

/**
 * @author: ciscn
 * @date:2019-07-02
 * @description:
 */
@Configuration
public class DubboListenBean {

    @Autowired
    private ApplicationContext context;

    @Value("${hb_dubbo.bind-address}")
    private String bindHost;

    @Value("${hb_dubbo.bind-port}")
    private String bindPort;

    @Value("${hb_dubbo.service}")
    private String serviceName;

    // server
    @Bean
    public AbstractServerConnectionFactory serverConnectionFactory() {
        TcpNioServerConnectionFactory tcpNioServerConnectionFactory = new TcpNioServerConnectionFactory(Integer.valueOf(bindPort));
        tcpNioServerConnectionFactory.setLocalAddress(bindHost);
        ByteArrayCrLfSerializer byteArrayCrLfSerializer = new ByteArrayCrLfSerializer();
        byteArrayCrLfSerializer.setMaxMessageSize(15 * 1024 * 1024);
        tcpNioServerConnectionFactory.setSerializer(byteArrayCrLfSerializer);
        tcpNioServerConnectionFactory.setDeserializer(byteArrayCrLfSerializer);
        return tcpNioServerConnectionFactory;
    }

    @Bean
    public MessageChannel requestChannel() {
        return new DirectChannel();
    }

    @Bean
    public TcpInboundGateway tcpInboundGateway() {
        TcpInboundGateway tcpInboundGateway = new TcpInboundGateway();
        tcpInboundGateway.setConnectionFactory(serverConnectionFactory());
        tcpInboundGateway.setRequestChannel(requestChannel());
        return tcpInboundGateway;
    }

    @Transformer(inputChannel = "requestChannel", outputChannel = "requestChannel2")
    public String serverConvert(byte[] bytes) {
        return new String(bytes);
    }

    @ServiceActivator(inputChannel = "requestChannel2")
    public String handleRequest(String msg) throws Exception {
        ObjectMapper objectMapper = new ObjectMapper();
        Map map = objectMapper.readValue(msg, Map.class);
        HashMap<String, Object> returnMap = new HashMap<>();

        if(map.get("opt").equals("call")) {
            String[] beanNames = serviceName.split("\\.");
            String beanName = beanNames[beanNames.length -1];
            beanName = beanName.substring(0, 1).toLowerCase() + beanName.substring(1) + "Impl";
            Object service = context.getBean(beanName);

            Method method = service.getClass().getDeclaredMethod((String) map.get("method"), HashMap.class);
            HashMap<String, Object> returnHashMap = (HashMap<String, Object>) method.invoke(service, map.get("parameter"));

            returnMap.put("data", returnHashMap);
        }

        returnMap.put("code", "100");

        return " " + objectMapper.writeValueAsString(returnMap);
    }
}

