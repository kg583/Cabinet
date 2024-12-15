package io.github.kg583;

import net.fabricmc.fabric.api.resource.SimpleSynchronousResourceReloadListener;
import net.minecraft.resource.Resource;
import net.minecraft.resource.ResourceManager;
import net.minecraft.util.Identifier;

import java.io.InputStream;
import java.util.Map;

public class FileListener implements SimpleSynchronousResourceReloadListener {
    @Override
    public Identifier getFabricId() {
        return Identifier.of(Cabinet.MOD_ID, "resources");
    }

    @Override
    public void reload(ResourceManager manager) {
        for (Map.Entry<Identifier, Resource> entry : manager.findResources("test", path -> true).entrySet()) {
            var id = entry.getKey();
            var resource = entry.getValue();

            try (InputStream stream = resource.getInputStream()) {
                Cabinet.LOGGER.info("Loaded {}", id.toString());
            } catch (Exception e) {
                Cabinet.LOGGER.error("Error occurred while loading file {}", id.toString(), e);
            }
        }
    }
}
