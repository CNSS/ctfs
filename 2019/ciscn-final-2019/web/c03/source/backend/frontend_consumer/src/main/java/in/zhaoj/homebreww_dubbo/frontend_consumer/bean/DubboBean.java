package in.zhaoj.homebreww_dubbo.frontend_consumer.bean;

import com.fasterxml.jackson.core.JsonProcessingException;
import in.zhaoj.homebreww_dubbo.frontend_consumer.compoment.ServiceComponent;
import in.zhaoj.homebreww_dubbo.frontend_consumer.util.JSONUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.integration.annotation.MessagingGateway;
import org.springframework.integration.annotation.ServiceActivator;
import org.springframework.integration.annotation.Transformer;
import org.springframework.integration.ip.tcp.TcpReceivingChannelAdapter;
import org.springframework.integration.ip.tcp.TcpSendingMessageHandler;
import org.springframework.integration.ip.tcp.connection.AbstractClientConnectionFactory;
import org.springframework.integration.ip.tcp.connection.TcpNioClientConnectionFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.HashMap;

/**
 * @author: ciscn
 * @date:2019-07-02
 * @description:
 */
@Configuration
public class DubboBean {
    @Autowired
    private Gateway gateway;

    @Autowired
    private JSONUtil jsonUtil;

    @Autowired
    private ServiceComponent serviceComponent;

    @Value("${hb_dubbo.reg-address}")
    private String host;

    @Value("${hb_dubbo.reg-port}")
    private String port;

    @Scheduled(fixedDelay = 10000L)
    public void sendMessageJob() {
        HashMap<String, Object> returnMap = new HashMap<>();
        returnMap.put("opt", "all");

        String msg = null;
        try {
            msg = jsonUtil.encode(returnMap);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }

        gateway.sendMessage(msg);
    }

    // client
    @Bean
    public AbstractClientConnectionFactory clientConnectionFactory() {
        return new TcpNioClientConnectionFactory(host, Integer.valueOf(port));
    }

    @Component
    @MessagingGateway(defaultRequestChannel = "sendMessageChannel")
    public interface Gateway {
        void sendMessage(String message);
    }

    @Bean
    @ServiceActivator(inputChannel = "sendMessageChannel")
    public TcpSendingMessageHandler tcpSendingMessageHandler() {
        TcpSendingMessageHandler tcpSendingMessageHandler = new TcpSendingMessageHandler();
        tcpSendingMessageHandler.setConnectionFactory(clientConnectionFactory());
        return tcpSendingMessageHandler;
    }

    @Bean
    public TcpReceivingChannelAdapter tcpReceivingChannelAdapter() {
        TcpReceivingChannelAdapter tcpReceivingChannelAdapter = new TcpReceivingChannelAdapter();
        tcpReceivingChannelAdapter.setConnectionFactory(clientConnectionFactory());
        tcpReceivingChannelAdapter.setOutputChannelName("outputChannel");
        return tcpReceivingChannelAdapter;
    }

    @Transformer(inputChannel = "outputChannel", outputChannel = "outputChannel2")
    public String clientConvert(byte[] bytes) {
        return new String(bytes);
    }

    @ServiceActivator(inputChannel = "outputChannel2")
    public String handleResponse(String msg) throws Exception {
        HashMap<String, Object> hashMap = this.jsonUtil.decode(msg);
        this.serviceComponent.setNodesHashMap((HashMap<String, Object>) hashMap.get("data"));
        return null;
    }

}
