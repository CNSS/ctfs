package in.zhaoj.homebreww_dubbo.frontend_consumer.util;

import org.springframework.stereotype.Component;

import java.nio.charset.StandardCharsets;
import java.util.Base64;

/**
 * @author: ciscn
 * @date:2018/8/9
 * @description:
 */
@Component
public class BASE64Util {
    /**
     * Base64 解码
     *
     * @param raw_text
     * @return
     */
    public String decode(String raw_text) {
        return new String(decodeToByte(raw_text), StandardCharsets.UTF_8);
    }

    /**
     * Base64 编码
     *
     * @param raw_text
     * @return
     */
    public String encode(byte[] raw_text) {
        return new String(encodeToByte(raw_text), StandardCharsets.UTF_8);
    }

    /**
     * Base64 编码
     *
     * @param raw_text
     * @return
     */
    public String encode(String raw_text) {
        return new String(encodeToByte(raw_text), StandardCharsets.UTF_8);
    }

    /**
     * Base64 解码
     *
     * @param raw_text
     * @return
     */
    public byte[] decodeToByte(String raw_text) {
        byte[] asBytes = Base64.getDecoder().decode(raw_text);
        return asBytes;
    }

    /**
     * Base64 编码
     *
     * @param raw_text
     * @return
     */
    public byte[] encodeToByte(String raw_text) {
        byte[] asBytes = Base64.getEncoder().encode(raw_text.getBytes());
        return asBytes;
    }

    /**
     * Base64 编码
     *
     * @param raw_text
     * @return
     */
    public byte[] encodeToByte(byte[] raw_text) {
        byte[] asBytes = Base64.getEncoder().encode(raw_text);
        return asBytes;
    }
}
