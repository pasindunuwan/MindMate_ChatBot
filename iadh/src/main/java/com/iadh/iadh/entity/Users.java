package com.iadh.iadh.entity;



import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import org.antlr.v4.runtime.misc.NotNull;



import java.util.UUID;

@Entity
@Table(name = "users")
public class Users {

    @Id
    @Column(name = "user_id", updatable = false, nullable = false)
    private String userId;



    @Column(name = "username", unique = true, nullable = false)
    private String username;



    @Column(name = "password", nullable = false)
    private String password;

    // Constructors
    public Users() {
        this.userId = UUID.randomUUID().toString();
    }

    public Users(String username, String password) {
        this.userId = UUID.randomUUID().toString();
        this.username = username;
        this.password = password;
    }

    // Getters and Setters
    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

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
