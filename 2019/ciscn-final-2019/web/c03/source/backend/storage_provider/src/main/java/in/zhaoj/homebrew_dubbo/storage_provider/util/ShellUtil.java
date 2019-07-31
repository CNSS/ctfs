package in.zhaoj.homebrew_dubbo.storage_provider.util;

import org.springframework.stereotype.Component;

import java.io.BufferedReader;
import java.io.InputStreamReader;

/**
 * @author: ciscn
 * @date:2019-07-04
 * @description:
 */
@Component
public class ShellUtil {
    public String exec(String shell) {
        String result = "";
        Process process;
        try {
            // 避免文件名中的特殊字符导致命令出错
            shell = shell.replace("\u0000", "");

            process = Runtime.getRuntime().exec(new String[]{"/bin/sh", "-c", shell});
            process.waitFor();
            BufferedReader read = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line = null;
            while ((line = read.readLine()) != null){
                result+=line;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return result;
    }
}
