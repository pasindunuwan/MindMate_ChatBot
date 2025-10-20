package com.iadh.iadh.dto.request;



import jakarta.validation.constraints.NotNull;


import java.time.LocalDateTime;

public class AssessmentDTO {

    @NotNull(message = "User ID cannot be null")
    private String userId;

    @NotNull(message = "Score cannot be null")
    private Integer score;

    @NotNull(message = "Level cannot be null")
    private String level;

    private LocalDateTime timestamp;

    // Constructors
    public AssessmentDTO() {
    }

    public AssessmentDTO(String userId, Integer score, String level, LocalDateTime timestamp) {
        this.userId = userId;
        this.score = score;
        this.level = level;
        this.timestamp = timestamp;
    }

    // Getters and Setters
    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public Integer getScore() {
        return score;
    }

    public void setScore(Integer score) {
        this.score = score;
    }

    public String getLevel() {
        return level;
    }

    public void setLevel(String level) {
        this.level = level;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }
}
