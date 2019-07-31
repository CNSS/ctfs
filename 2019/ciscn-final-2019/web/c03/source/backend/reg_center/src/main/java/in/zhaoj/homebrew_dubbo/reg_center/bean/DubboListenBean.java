package in.zhaoj.homebrew_dubbo.reg_center.bean;

import com.fasterxml.jackson.databind.ObjectMapper;
import in.zhaoj.homebrew_dubbo.reg_center.compoment.ServicesComponent;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.integration.annotation.ServiceActivator;
import org.springframework.integration.annotation.Transformer;
import org.springframework.integration.channel.DirectChannel;
import org.springframework.integration.ip.tcp.TcpInboundGateway;
import org.springframework.integration.ip.tcp.connection.AbstractServerConnectionFactory;
import org.springframework.integration.ip.tcp.connection.TcpNioServerConnectionFactory;
import org.springframework.messaging.MessageChannel;

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
    private ServicesComponent servicesComponent;

    @Value("${hb_dubbo.bind-address}")
    private String host;

    @Value("${hb_dubbo.bind-port}")
    private String port;

    // server
    @Bean
    public AbstractServerConnectionFactory serverConnectionFactory() {
        TcpNioServerConnectionFactory tcpNioServerConnectionFactory = new TcpNioServerConnectionFactory(Integer.valueOf(port));
        tcpNioServerConnectionFactory.setLocalAddress(host);
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

        if(map.get("opt").equals("reg")) {
            this.servicesComponent.regServiceNode((String) map.get("service"), (String) map.get("host"), Integer.valueOf((String) map.get("port")));
        }

        if(map.get("opt").equals("call")) {
            returnMap.put("data", this.servicesComponent.pullServiceNode((String) map.get("service")));
        }

        if(map.get("opt").equals("all")) {
            returnMap.put("data", this.servicesComponent.pullAllServiceNode());
        }

        returnMap.put("code", "100");
        return objectMapper.writeValueAsString(returnMap);
    }
}
