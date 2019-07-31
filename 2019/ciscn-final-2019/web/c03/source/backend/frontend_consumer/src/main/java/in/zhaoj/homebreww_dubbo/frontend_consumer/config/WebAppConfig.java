package in.zhaoj.homebreww_dubbo.frontend_consumer.config;

import in.zhaoj.homebreww_dubbo.frontend_consumer.interceptor.ApiCorsInterceptor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.web.context.request.async.TimeoutCallableProcessingInterceptor;
import org.springframework.web.servlet.config.annotation.AsyncSupportConfigurer;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * @author: ciscn
 * @date:2018/8/9
 * @description:
 */
@Configuration
@EnableAsync
//s@EnableCaching
public class WebAppConfig implements WebMvcConfigurer {
    /**
     * 为了依赖注入
     *
     * @return
     */

    @Override
    public void configureAsyncSupport(final AsyncSupportConfigurer configurer) {
        configurer.setDefaultTimeout(20000);
        configurer.registerCallableInterceptors(timeoutInterceptor());
    }
    @Bean
    public TimeoutCallableProcessingInterceptor timeoutInterceptor() {
        return new TimeoutCallableProcessingInterceptor();
    }

    @Bean
    public ApiCorsInterceptor apiCorsInterceptor() {
        return new ApiCorsInterceptor();
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // 多个拦截器组成一个拦截器链
        registry.addInterceptor(this.apiCorsInterceptor()).addPathPatterns("/api/**");
    }

    @Override
    //重写父类提供的跨域请求处理的接口
    public void addCorsMappings(CorsRegistry registry) {
        //添加映射路径
        registry.addMapping("/api/**")
                //放行哪些原始域
                .allowedOrigins("*")
                //是否发送Cookie信息
                .allowCredentials(true)
                //放行哪些原始域(请求方式)
                .allowedMethods("GET", "POST", "PUT", "DELETE", "PATCH")
                //放行哪些原始域(头部信息)
                .allowedHeaders("*");
    }
}
