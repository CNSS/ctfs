package in.zhaoj.homebreww_dubbo.frontend_consumer.util;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.util.DigestUtils;

import java.io.IOException;
import java.util.HashMap;

/**
 * @author: ciscn
 * @date:2019-07-04
 * @description:
 */
@Component
public class FileSignUtil {

    @Value("${file.sign_key}")
    private String secretKey;

    @Autowired
    private BASE64Util base64Util;

    @Autowired
    private JSONUtil jsonUtil;

    private byte[] arrayUnion(byte[] a, byte[] b) {
        byte[] c = new byte[a.length + b.length];
        System.arraycopy(a, 0, c, 0, a.length);
        System.arraycopy(b, 0, c, a.length, b.length);
        return c;
    }

    private String getSign(byte[] filename) {
        return base64Util.encode(encrypt(arrayUnion(secretKey.getBytes(), filename)));
    }

    public String getToken(byte[] fileName) {
        try {
            HashMap<String, Object> jsonHashMap = new HashMap<>();
            jsonHashMap.put("id", base64Util.encode(fileName));
            jsonHashMap.put("sign", getSign(fileName));
            String jsonStr = jsonUtil.encode(jsonHashMap);
            return base64Util.encode(jsonStr);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public byte[] verifyToken(String token) {
        try {
            HashMap<String, Object> jsonHashMap = jsonUtil.decode(base64Util.decode(token));
            byte[] id = base64Util.decodeToByte((String) jsonHashMap.get("id"));
            String sign = (String) jsonHashMap.get("sign");
            if(verify(id, sign)) {
                return id;
            } else {
                return null;
            }
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    private boolean verify(byte[] fileName, String sign) {
        return getSign(fileName).equals(sign);
    }

    public String byteToHex(byte num) {
        char[] hexDigits = new char[2];
        hexDigits[0] = Character.forDigit((num >> 4) & 0xF, 16);
        hexDigits[1] = Character.forDigit((num & 0xF), 16);
        return new String(hexDigits);
    }

    private String encrypt(byte[] raw_text) {
        return DigestUtils.md5DigestAsHex(raw_text);
    }
}
