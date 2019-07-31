package in.zhaoj.homebrew_dubbo.reg_center;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class RegCenterApplication {

    public static void main(String[] args) {
        SpringApplication.run(RegCenterApplication.class, args);
    }

}
