package io.github.kg583.compile;

import java.util.ArrayList;

public class CabinetCommand {
    private final ArrayList<String> tokens;

    public CabinetCommand() {
        this.tokens = new ArrayList<>();
    }

    public String command() {
        return this.tokens.getFirst();
    }

    public void pushToken(String token) {
        this.tokens.add(token);
    }
}
