package in.zhaoj.homebrew_dubbo.flag_provider.service;

import java.util.HashMap;

/**
 * @author: ciscn
 * @date:2019-07-03
 * @description:
 */
public interface FlagService {
    HashMap<String, Object> getFlag(HashMap<String, Object> parameter);
}
