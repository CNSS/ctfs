package in.zhaoj.homebrew_dubbo.flag_provider;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class FlagProviderApplication {

    public static void main(String[] args) {
        SpringApplication.run(FlagProviderApplication.class, args);
    }

}
