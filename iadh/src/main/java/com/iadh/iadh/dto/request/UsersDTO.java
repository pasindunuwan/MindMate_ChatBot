package com.iadh.iadh.dto.request;


import org.antlr.v4.runtime.misc.NotNull;

public class UsersDTO {


    private String username;

    private String password;

    // Constructors
    public UsersDTO() {
    }

    public UsersDTO(String username, String password) {
        this.username = username;
        this.password = password;
    }

    // Getters and Setters
    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}
