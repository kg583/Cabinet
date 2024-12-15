package io.github.kg583;

import net.fabricmc.api.ModInitializer;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Cabinet implements ModInitializer {
	public static final String MOD_ID = "cabinet";
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	@Override
	public void onInitialize() {
		// Begin init
		LOGGER.info("Initializing Cabinet...");
	}
}