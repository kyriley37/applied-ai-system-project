# Advanced Mood Machine - Architecture Diagrams

This file contains Mermaid.js code for system architecture diagrams.
Paste each diagram into https://mermaid.live to generate PNG images for the `/assets` folder.

---

## Diagram 1: System Architecture Overview

```mermaid
graph TB
    subgraph Input["Input Layer"]
        UI["Interactive UI / Batch Input"]
    end
    
    subgraph Core["Core Intelligence Layer"]
        Agent["🧠 MoodAgent<br/>(Agentic Workflow)"]
    end
    
    subgraph Processing["Processing Components"]
        Analyzer["📊 MoodAnalyzer<br/>(Rule-Based Scoring)"]
        RAG["🔍 MoodKnowledgeBase<br/>(RAG Retrieval)"]
    end
    
    subgraph Support["Support Systems"]
        Logger["📝 MoodMachineLogger<br/>(Logging & Guardrails)"]
        Validator["✅ MoodMachineValidator<br/>(Testing & Validation)"]
    end
    
    subgraph Data["Data Layer"]
        Dataset["📚 Dataset<br/>(Posts & Labels)"]
    end
    
    subgraph Output["Output Layer"]
        Result["🎯 Prediction + Confidence + Reasoning"]
        Logs["📋 Logs Directory"]
    end
    
    UI --> Agent
    Agent --> Analyzer
    Agent --> RAG
    Analyzer --> Logger
    RAG --> Logger
    Dataset --> RAG
    Dataset --> Validator
    Agent --> Result
    Logger --> Logs
    Validator --> Logs
    
    style Agent fill:#4CAF50,stroke:#2E7D32,color:#fff
    style Analyzer fill:#2196F3,stroke:#1565C0,color:#fff
    style RAG fill:#FF9800,stroke:#E65100,color:#fff
    style Logger fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style Validator fill:#F44336,stroke:#C62828,color:#fff
    style Result fill:#4CAF50,stroke:#2E7D32,color:#fff
```

---

## Diagram 2: Agentic Workflow - Step-by-Step Reasoning

```mermaid
sequenceDiagram
    participant User as User Input
    participant Agent as MoodAgent
    participant Analyzer as MoodAnalyzer
    participant KB as Knowledge Base
    participant Logger as Logger
    participant Output as Output Result
    
    User->>Agent: Provide text to analyze
    Note over Agent: Step 1: Preprocess
    Agent->>Analyzer: preprocess(text)
    Analyzer-->>Agent: tokens
    Agent->>Logger: Log preprocess step
    
    Note over Agent: Step 2: Retrieve Similar
    Agent->>KB: retrieve_similar(text)
    KB-->>Agent: similar posts + labels + scores
    Agent->>Logger: Log retrieval
    
    Note over Agent: Step 3: Score Text
    Agent->>Analyzer: score_text(text)
    Analyzer-->>Agent: numeric score
    Agent->>Logger: Log direct score
    
    Note over Agent: Step 4: Analyze Retrieved
    Agent->>KB: get_label_distribution(retrieved)
    KB-->>Agent: mood distribution
    Agent->>Logger: Log consensus
    
    Note over Agent: Step 5: Synthesize
    Agent->>Agent: Determine final mood<br/>Calculate confidence
    Agent->>Logger: Log synthesis
    
    Note over Agent: Step 6: Evaluate Confidence
    Agent->>Agent: Calibrate confidence score
    Agent->>Logger: Log confidence
    
    Agent->>Output: Return prediction dictionary
    Output-->>User: Display mood + confidence + reasoning
```

---

## Diagram 3: Component Interaction Diagram

```mermaid
graph LR
    subgraph Input["🔤 Input"]
        Text["Raw Text"]
    end
    
    subgraph Main["🎯 MoodAgent<br/>(Orchestrator)"]
        A1["Preprocess"]
        A2["Retrieve"]
        A3["Score"]
        A4["Analyze"]
        A5["Synthesize"]
        A6["Calibrate"]
    end
    
    subgraph Components["📦 Components"]
        MA["MoodAnalyzer"]
        KB["KnowledgeBase"]
        L["Logger"]
        V["Validator"]
    end
    
    subgraph Output["📊 Output"]
        Mood["Predicted Mood"]
        Conf["Confidence"]
        Reason["Reasoning"]
        Related["Similar Posts"]
    end
    
    Text --> A1
    A1 --> A2
    A2 --> A3
    A3 --> A4
    A4 --> A5
    A5 --> A6
    
    A1 --> MA
    A3 --> MA
    A2 --> KB
    A4 --> KB
    
    MA --> L
    KB --> L
    A1 --> L
    A2 --> L
    A3 --> L
    A4 --> L
    A5 --> L
    A6 --> L
    
    A6 --> Mood
    A6 --> Conf
    A5 --> Reason
    A2 --> Related
    
    V -.-> MA
    V -.-> KB
    V -.-> L
    
    style A1 fill:#E3F2FD,stroke:#1976D2
    style A2 fill:#FFF3E0,stroke:#F57C00
    style A3 fill:#E8F5E9,stroke:#388E3C
    style A4 fill:#F3E5F5,stroke:#7B1FA2
    style A5 fill:#FCE4EC,stroke:#C2185B
    style A6 fill:#FFF9C4,stroke:#F57F17
```

---

## Diagram 4: Data Flow - From Input to Output

```mermaid
flowchart TD
    Input["📥 User Input: Text"] -->|Pass to Agent| Step1["⚙️ Step 1: Preprocess<br/>Remove punctuation, handle emojis"]
    
    Step1 -->|Tokenized text| Step2["🔍 Step 2: Retrieve Similar<br/>Search knowledge base"]
    
    Step2 -->|Similar posts + labels| Step3["📊 Step 3: Score Direct<br/>Count positive/negative words"]
    
    Step3 -->|Numeric score| Step4["📈 Step 4: Analyze Retrieved<br/>Get mood distribution"]
    
    Step4 -->|Consensus mood| Step5["🔄 Step 5: Synthesize<br/>Combine direct + retrieved"]
    
    Step5 -->|Preliminary prediction| Step6["⭐ Step 6: Calibrate<br/>Confidence scoring"]
    
    Step6 -->|Final mood + confidence| Output["📤 Output<br/>Mood + Confidence + Reasoning<br/>+ Retrieved Posts"]
    
    Step1 -->|Token info| LogA["📝 Log Step 1"]
    Step2 -->|Retrieval details| LogB["📝 Log Step 2"]
    Step3 -->|Score details| LogC["📝 Log Step 3"]
    Step4 -->|Distribution| LogD["📝 Log Step 4"]
    Step5 -->|Synthesis| LogE["📝 Log Step 5"]
    Step6 -->|Confidence| LogF["📝 Log Step 6"]
    
    LogA --> Logfile["📋 Log File<br/>logs/mood_machine_*.log"]
    LogB --> Logfile
    LogC --> Logfile
    LogD --> Logfile
    LogE --> Logfile
    LogF --> Logfile
    
    style Input fill:#C8E6C9,stroke:#2E7D32,color:#000
    style Output fill:#81C784,stroke:#1B5E20,color:#fff
    style Step1 fill:#BBDEFB,stroke:#0D47A1
    style Step2 fill:#FFE0B2,stroke:#E65100
    style Step3 fill:#C8E6C9,stroke:#1B5E20
    style Step4 fill:#F8BBD0,stroke:#880E4F
    style Step5 fill:#FFCCBC,stroke:#BF360C
    style Step6 fill:#FFF9C4,stroke:#F57F17
    style Logfile fill:#E1BEE7,stroke:#6A1B9A,color:#000
```

---

## Diagram 5: RAG System Architecture

```mermaid
graph TB
    subgraph KB["🗂️ Knowledge Base<br/>(MoodKnowledgeBase)"]
        Posts["📚 SAMPLE_POSTS<br/>[post1, post2, ...]"]
        Labels["🏷️ TRUE_LABELS<br/>[positive, negative, ...]"]
    end
    
    subgraph Query["🔍 Query Processing"]
        Input["User Input Text"]
        Similarity["Similarity Computation<br/>(Word Overlap)"]
    end
    
    subgraph Retrieval["📊 Retrieval Engine"]
        Rank["Rank by Similarity"]
        Select["Select Top-K<br/>(k=3)"]
    end
    
    subgraph Analysis["📈 Analysis"]
        Distribution["Get Label Distribution<br/>Count moods in retrieved"]
        Consensus["Find Consensus<br/>Most common mood"]
    end
    
    subgraph Result["🎯 Retrieved Context"]
        Similar["Similar Posts<br/>+ Labels + Scores"]
        Mood["Consensus Mood<br/>for synthesis"]
    end
    
    Input --> Similarity
    Posts --> Similarity
    Similarity --> Rank
    Rank --> Select
    Select --> Analysis
    Labels --> Distribution
    Distribution --> Consensus
    Consensus --> Mood
    Select --> Similar
    
    Similar --> Result
    Mood --> Result
    
    style KB fill:#FFE0B2,stroke:#E65100,color:#000
    style Query fill:#BBDEFB,stroke:#0D47A1
    style Retrieval fill:#C8E6C9,stroke:#1B5E20,color:#000
    style Analysis fill:#F8BBD0,stroke:#880E4F,color:#000
    style Result fill:#FFCCBC,stroke:#BF360C,color:#000
```

---

## Diagram 6: Testing & Validation Framework

```mermaid
graph TB
    subgraph Validator["✅ MoodMachineValidator"]
        T1["Test 1: Consistency<br/>Same input → Same output"]
        T2["Test 2: Accuracy<br/>Against TRUE_LABELS"]
        T3["Test 3: Calibration<br/>Confidence vs Correctness"]
        T4["Test 4: Edge Cases<br/>Empty, special chars, long text"]
    end
    
    subgraph Dataset["📚 Test Data"]
        SAMPLE["SAMPLE_POSTS<br/>(6 posts)"]
        TRUE["TRUE_LABELS<br/>(6 labels)"]
    end
    
    subgraph Testing["🧪 Testing Process"]
        Run["Run Tests"]
        Measure["Measure Results"]
        Report["Generate Report"]
    end
    
    subgraph Metrics["📊 Metrics Tracked"]
        Acc["Accuracy %"]
        Conf["Confidence Scores"]
        Cons["Consistency %"]
        Cal["Calibration Status"]
    end
    
    SAMPLE --> T1
    SAMPLE --> T2
    SAMPLE --> T3
    SAMPLE --> T4
    TRUE --> T2
    
    T1 --> Run
    T2 --> Run
    T3 --> Run
    T4 --> Run
    
    Run --> Measure
    Measure --> Acc
    Measure --> Conf
    Measure --> Cons
    Measure --> Cal
    
    Acc --> Report
    Conf --> Report
    Cons --> Report
    Cal --> Report
    
    Report -->|Print| Terminal["Console Output"]
    Report -->|Log| Logfile["Log File"]
    
    style Validator fill:#F3E5F5,stroke:#6A1B9A,color:#000
    style Dataset fill:#E3F2FD,stroke:#0D47A1,color:#000
    style Metrics fill:#FFF9C4,stroke:#F57F17,color:#000
    style Terminal fill:#C8E6C9,stroke:#1B5E20,color:#000
    style Logfile fill:#FFCCBC,stroke:#BF360C,color:#000
```

---

## Diagram 7: Confidence Score Calibration

```mermaid
graph LR
    subgraph Input["📥 Analysis Input"]
        Direct["Direct Score from<br/>Rule Analyzer"]
        Retrieved["Consensus from<br/>Retrieved Posts"]
    end
    
    subgraph Logic["🧠 Confidence Logic"]
        Agreement{"Direct Label<br/>== Consensus?"}
        HighConf["Start: 0.9"]
        LowConf["Start: 0.7"]
        Boost["+ 0.1 if strong<br/>agreement in retrieved"]
        Cap["Cap at 1.0"]
    end
    
    subgraph Output["📊 Final Output"]
        Confidence["Confidence Score<br/>[0.0 - 1.0]"]
    end
    
    Direct --> Agreement
    Retrieved --> Agreement
    
    Agreement -->|Yes| HighConf
    Agreement -->|No| LowConf
    
    HighConf --> Boost
    LowConf --> Boost
    Boost --> Cap
    Cap --> Confidence
    
    style Agreement fill:#FFF9C4,stroke:#F57F17,color:#000
    style HighConf fill:#C8E6C9,stroke:#1B5E20,color:#000
    style LowConf fill:#FFCCBC,stroke:#BF360C,color:#000
    style Confidence fill:#81C784,stroke:#1B5E20,color:#fff
```

---

## Diagram 8: Class Diagram - Component Relationships

```mermaid
classDiagram
    class MoodAnalyzer {
        -positive_words: set
        -negative_words: set
        +preprocess(text) str[]
        +score_text(text) int
        +predict_label(text) str
        +explain(text) str
    }
    
    class MoodKnowledgeBase {
        -posts: list
        -labels: list
        -logger: MoodMachineLogger
        +retrieve_similar(query) tuple[]
        +get_label_distribution() dict
        -_compute_similarity() float
    }
    
    class MoodAgent {
        -rule_analyzer: MoodAnalyzer
        -knowledge_base: MoodKnowledgeBase
        -logger: MoodMachineLogger
        -step_count: int
        +analyze_mood(text) dict
        -_log_step() void
        -_get_default_label() str
        -_build_explanation() str
    }
    
    class MoodMachineLogger {
        -log_dir: str
        -logger: logging.Logger
        +log_event() void
        +log_agent_reasoning() void
        +log_mood_prediction() void
        +log_retrieval() void
        +log_error() void
        +log_info() void
    }
    
    class MoodMachineValidator {
        -agent: MoodAgent
        -logger: MoodMachineLogger
        -results: dict
        +test_consistency() dict
        +test_accuracy() dict
        +test_confidence_calibration() dict
        +test_edge_cases() dict
        +run_full_validation() dict
        +print_validation_report() void
    }
    
    MoodAgent --> MoodAnalyzer
    MoodAgent --> MoodKnowledgeBase
    MoodAgent --> MoodMachineLogger
    MoodAnalyzer --> MoodMachineLogger
    MoodKnowledgeBase --> MoodMachineLogger
    MoodMachineValidator --> MoodAgent
    MoodMachineValidator --> MoodMachineLogger
```

---

## How to Use These Diagrams

1. **Copy each diagram code** (the `mermaid` block)
2. **Go to** https://mermaid.live
3. **Paste the code** into the editor
4. **Export as PNG** using the download button
5. **Save to** `/assets/` folder with descriptive names:
   - `system_architecture.png`
   - `agentic_workflow.png`
   - `component_interaction.png`
   - `data_flow.png`
   - `rag_system.png`
   - `testing_framework.png`
   - `confidence_calibration.png`
   - `class_diagram.png`

---

## Notes

- Each diagram shows a different perspective of the system
- Colors indicate different functional areas
- Diagrams are designed to be clear and educational
- Use them in your documentation and presentations
