package com.example.webml.model;

import jakarta.persistence.*;

import java.util.List;

@Entity
public class InputData {
    @Id
    @GeneratedValue
    private long nodeID;
    private String clientID;
    private String organizationID;
    private String segment;
    private String role;
    private int organizations;
    private String currentMethod;
    private boolean mobileApp;
    @Embedded
    private Signatures signatures;
    @ElementCollection
    private List<String> availableMethods;
    private long claims;

    @Embeddable
    public static class Signatures {
        @Embedded
        private DocumentCounts common;
        @Embedded
        private DocumentCounts special;

        public DocumentCounts getCommon() { return common; }
        public void setCommon(DocumentCounts common) { this.common = common; }
        public DocumentCounts getSpecial() { return special; }
        public void setSpecial(DocumentCounts special) { this.special = special; }
    }

    @Embeddable
    public static class DocumentCounts {
        @Column(name = "mobile_count", insertable=false, updatable=false)
        private long mobile;
        @Column(name = "web_count", insertable=false, updatable=false)
        private long web;

        public long getMobile() { return mobile; }
        public void setMobile(long mobile) { this.mobile = mobile; }
        public long getWeb() { return web; }
        public void setWeb(long web) { this.web = web; }
    }

    public long getNodeID() { return nodeID; }
    public void setNodeID(long nodeID) { this.nodeID = nodeID; }
    public String getClientID() { return clientID; }
    public void setClientID(String clientID) { this.clientID = clientID; }
    public String getOrganizationID() { return organizationID; }
    public void setOrganizationID(String organizationID) { this.organizationID = organizationID; }
    public String getSegment() { return segment; }
    public void setSegment(String segment) { this.segment = segment; }
    public String getRole() { return role; }
    public void setRole(String role) { this.role = role; }
    public int getOrganizations() { return organizations; }
    public void setOrganizations(int organizations) { this.organizations = organizations; }
    public String getCurrentMethod() { return currentMethod; }
    public void setCurrentMethod(String currentMethod) { this.currentMethod = currentMethod; }
    public boolean isMobileApp() { return mobileApp; }
    public void setMobileApp(boolean mobileApp) { this.mobileApp = mobileApp; }
    public Signatures getSignatures() { return signatures; }
    public void setSignatures(Signatures signatures) { this.signatures = signatures; }
    public List<String> getAvailableMethods() { return availableMethods; }
    public void setAvailableMethods(List<String> availableMethods) { this.availableMethods = availableMethods; }
    public long getClaims() { return claims; }
    public void setClaims(long claims) { this.claims = claims; }
}

