package in.zhaoj.homebrew_dubbo.storage_provider;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class StorageProviderApplication {

    public static void main(String[] args) {
        SpringApplication.run(StorageProviderApplication.class, args);
    }

}
