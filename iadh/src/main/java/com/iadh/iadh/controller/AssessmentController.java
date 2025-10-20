package com.iadh.iadh.controller;



import com.iadh.iadh.dto.request.AssessmentDTO;
import com.iadh.iadh.service.AssessmentService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


import java.util.Collections;
import java.util.List;

@RestController
@RequestMapping("/api/assessments")
public class AssessmentController {

    @Autowired
    private AssessmentService assessmentService;

    @PostMapping("/save")
    public ResponseEntity<String> saveAssessment(@Valid @RequestBody AssessmentDTO assessmentDTO) {
        try {
            assessmentService.saveAssessment(assessmentDTO);
            return ResponseEntity.ok("Assessment saved successfully.");
        } catch (IllegalArgumentException e) {
            return ResponseEntity.status(400).body(e.getMessage());
        }
    }

    @GetMapping("/{userId}")
    public ResponseEntity<List<AssessmentDTO>> getAssessments(@PathVariable String userId) {
        try {
            List<AssessmentDTO> assessments = assessmentService.getAssessmentsByUserId(userId);
            return ResponseEntity.ok(assessments);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.status(400).body( Collections.emptyList());
        }
    }
}
