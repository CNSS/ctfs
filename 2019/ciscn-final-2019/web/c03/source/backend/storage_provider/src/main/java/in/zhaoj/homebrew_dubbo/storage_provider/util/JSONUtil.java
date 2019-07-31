package in.zhaoj.homebrew_dubbo.storage_provider.util;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.HashMap;

/**
 * @author: ciscn
 * @date:2018/8/9
 * @description:
 */
@Component
public class JSONUtil {
    /**
     * JSON 解码
     *
     * @param json_string
     * @return
     * @throws IOException
     */
    public HashMap<String, Object> decode(String json_string) throws IOException {
        ObjectMapper mapper = new ObjectMapper();

        HashMap<String, Object> map = new HashMap<String, Object>();

        // convert JSON string to Map
        map = mapper.readValue(json_string, new TypeReference<HashMap<String, Object>>() {
        });

        return map;
    }

    public String encode(Object map) throws JsonProcessingException {
        ObjectMapper mapper = new ObjectMapper();

        return mapper.writer().writeValueAsString(map);
    }
}
