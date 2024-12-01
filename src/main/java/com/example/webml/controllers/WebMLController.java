package com.example.webml.controllers;

import com.example.webml.model.InputData;
import com.example.webml.repositories.InputDataRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.util.ArrayList;

@Controller
public class WebMLController implements CommandLineRunner {
    private final InputDataRepository inputDataRepository;
    private final ObjectMapper objectMapper = new ObjectMapper();

    public WebMLController(InputDataRepository inputDataRepository) {
        this.inputDataRepository = inputDataRepository;
    }

    private String runScript(InputData inputData) {
        try {
            String jsonData = objectMapper.writeValueAsString(inputData);
            ProcessBuilder processBuilder = new ProcessBuilder("python", "src\\python\\predict.py");
            Process process = processBuilder.start();;
            OutputStream os = process.getOutputStream();
            os.write(jsonData.getBytes());
            os.flush();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
            return output.toString().trim();
        } catch (Exception e) {
            return null;
        }
    }

    private String parseScriptOutput(String scriptOutput) {
        return scriptOutput;
    }

    @GetMapping({"/", "index"})
    String index(Model model) {
        if (!model.containsAttribute("data")) {
            InputData data = new InputData();
            data.setAvailableMethods(new ArrayList<>());
            data.setSignatures(new InputData.Signatures());
            data.getSignatures().setCommon(new InputData.DocumentCounts());
            data.getSignatures().setSpecial(new InputData.DocumentCounts());
            model.addAttribute("data", data);
        }
        return "index";
    }

    @PostMapping("/submit")
    public String submit(@ModelAttribute InputData inputData, RedirectAttributes redirectAttributes) {
        String scriptOutput = runScript(inputData);
        if (scriptOutput != null) {
            redirectAttributes.addFlashAttribute("result", parseScriptOutput(scriptOutput));
        } else {
            redirectAttributes.addFlashAttribute("result", "Ошибка выполнения.");
        }
        redirectAttributes.addFlashAttribute("data", inputData);

        inputDataRepository.save(inputData);
        return "redirect:/index";
    }

    @Override
    public void run(String... args) throws Exception {
        //inputDataRepository.save(null);
    }
}
