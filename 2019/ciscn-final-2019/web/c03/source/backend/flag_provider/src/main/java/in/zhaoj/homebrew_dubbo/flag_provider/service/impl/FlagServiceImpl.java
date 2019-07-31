package in.zhaoj.homebrew_dubbo.flag_provider.service.impl;

import in.zhaoj.homebrew_dubbo.flag_provider.service.FlagService;
import org.apache.commons.io.IOUtils;
import org.springframework.stereotype.Service;

import java.io.FileInputStream;
import java.util.HashMap;

/**
 * @author: ciscn
 * @date:2019-07-03
 * @description:
 */
@Service
public class FlagServiceImpl implements FlagService {
    @Override
    public HashMap<String, Object> getFlag(HashMap<String, Object> parameter) {
        HashMap<String, Object> returnHashmap = new HashMap<>();
        try {
            FileInputStream fis = new FileInputStream("/flag");
            String data = IOUtils.toString(fis, "UTF-8");

            returnHashmap.put("flag", data);
            return returnHashmap;
        } catch (Exception e) {
            e.printStackTrace();
            return returnHashmap;
        }
    }
}
