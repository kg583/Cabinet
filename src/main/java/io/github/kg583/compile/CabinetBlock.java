package io.github.kg583.compile;

import java.util.ArrayList;

public abstract class CabinetBlock {
    public String name;
    public ArrayList<CabinetCommand> commands;

    public CabinetBlock(String name) {
        this.name = name;
        this.commands = new ArrayList<>();
    }
}
