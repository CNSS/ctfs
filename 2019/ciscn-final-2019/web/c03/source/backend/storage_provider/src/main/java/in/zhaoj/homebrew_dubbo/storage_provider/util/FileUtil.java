package in.zhaoj.homebrew_dubbo.storage_provider.util;

import org.springframework.stereotype.Component;

import java.io.File;
import java.util.List;

/**
 * @author: ciscn
 * @date:2019-07-04
 * @description:
 */
@Component
public class FileUtil {
    public void list(final File folder, List<String> result) {
        for (final File f : folder.listFiles()) {

            if (f.isDirectory()) {
                list(f, result);
            }

            if (f.isFile()) {
                result.add(f.getPath().replace(folder.getPath() + "/", ""));
            }

        }
    }

    public static boolean deleteDir(File dir) {
        if (dir.isDirectory()) {
            String[] children = dir.list();

            for (int i=0; i<children.length; i++) {
                boolean success = deleteDir(new File(dir, children[i]));
                if (!success) {
                    return false;
                }
            }
        }
        // 目录此时为空，可以删除
        return dir.delete();
    }
}
