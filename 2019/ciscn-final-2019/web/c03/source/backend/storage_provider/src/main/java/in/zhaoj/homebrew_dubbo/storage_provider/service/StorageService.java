package in.zhaoj.homebrew_dubbo.storage_provider.service;

import java.util.HashMap;

public interface StorageService {
    HashMap<String, Object> putFile(HashMap<String, Object> parameter);

    HashMap<String, Object> getFileLists(HashMap<String, Object> parameter);

    HashMap<String, Object> deleteFile(HashMap<String, Object> parameter);

    HashMap<String, Object> readFile(HashMap<String, Object> parameter);
}
