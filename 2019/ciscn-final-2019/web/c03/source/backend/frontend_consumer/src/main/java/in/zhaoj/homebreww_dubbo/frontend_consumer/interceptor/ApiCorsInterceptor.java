package in.zhaoj.homebreww_dubbo.frontend_consumer.interceptor;

import org.springframework.http.HttpHeaders;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * @author: ciscn
 * @date:2018/8/9
 * @description:
 */
public class ApiCorsInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        if (request.getHeader(HttpHeaders.ORIGIN) != null) {
            response.addHeader("Access-Control-Allow-Origin", "*");
            response.addHeader("Access-Control-Allow-Credentials", "true");
            response.addHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE, PUT, HEAD, PATCH");
            response.addHeader("Access-Control-Allow-Headers", "Content-Type,Key");
            response.addHeader("Access-Control-Max-Age", "3600");
        }
        return true;
    }
}
