package in.zhaoj.homebreww_dubbo.frontend_consumer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class FrontendConsumerApplication {

    public static void main(String[] args) {
        SpringApplication.run(FrontendConsumerApplication.class, args);
    }

}
