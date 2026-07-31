-- 1. Create the Subjects Table (The Employees/Targets)
CREATE TABLE Subjects (
    SubjectID INT IDENTITY(1,1) PRIMARY KEY,
    EmailAddress VARCHAR(255) UNIQUE NOT NULL,
    Department VARCHAR(100),
    RiskBaselineScore DECIMAL(5,2) DEFAULT 0.00,
    CreatedAt DATETIME DEFAULT GETDATE()
);

-- 2. Create the Communications Evidence Table (UPDATED)
CREATE TABLE CommunicationsLog (
    LogID INT IDENTITY(1,1) PRIMARY KEY,
    SenderID INT FOREIGN KEY REFERENCES Subjects(SubjectID),
    ReceiverEmail VARCHAR(255) NOT NULL,
    CommunicationDate DATETIME NOT NULL,
    SubjectLine VARCHAR(500),
    ExtractedBody NVARCHAR(MAX) NOT NULL,
    IsAnalyzed BIT DEFAULT 0,
    -- NEW COLUMN: Stores the exact sentences that triggered psycholinguistic flags
    ExtractedEvidence NVARCHAR(MAX) NULL 
);

-- 3. Create the Psycholinguistic Incident Tracking Table
CREATE TABLE PsycholinguisticScores (
    ScoreID INT IDENTITY(1,1) PRIMARY KEY,
    LogID INT FOREIGN KEY REFERENCES CommunicationsLog(LogID),
    UrgencyScore DECIMAL(5,2) DEFAULT 0.00,
    CertaintyScore DECIMAL(5,2) DEFAULT 0.00,
    NegativeAffectScore DECIMAL(5,2) DEFAULT 0.00,
    SelfFocusScore DECIMAL(5,2) DEFAULT 0.00,
    FlaggedAsAnomaly BIT DEFAULT 0,
    AnalysisDate DATETIME DEFAULT GETDATE()
);

-- 4. Create the Evidence Attachments Table
CREATE TABLE QuarantinedAttachments (
    AttachmentID INT IDENTITY(1,1) PRIMARY KEY,
    LogID INT FOREIGN KEY REFERENCES CommunicationsLog(LogID),
    Filename VARCHAR(255) NOT NULL,
    StoragePath VARCHAR(500) NOT NULL,
    ExtractionDate DATETIME DEFAULT GETDATE()
);