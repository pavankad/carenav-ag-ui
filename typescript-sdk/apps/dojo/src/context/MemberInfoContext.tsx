"use client";
import React, { createContext, useContext, useState, ReactNode } from "react";

interface MemberInfoContextType {
  firstname: string;
  setFirstname: (v: string) => void;
  lastname: string;
  setLastname: (v: string) => void;
  dob: string;
  setDob: (v: string) => void;
}

const MemberInfoContext = createContext<MemberInfoContextType | undefined>(undefined);

export const MemberInfoProvider = ({ children }: { children: ReactNode }) => {
  const [firstname, setFirstname] = useState("");
  const [lastname, setLastname] = useState("");
  const [dob, setDob] = useState("");

  return (
    <MemberInfoContext.Provider value={{ firstname, setFirstname, lastname, setLastname, dob, setDob }}>
      {children}
    </MemberInfoContext.Provider>
  );
};

export const useMemberInfo = () => {
  const ctx = useContext(MemberInfoContext);
  if (!ctx) throw new Error("useMemberInfo must be used within a MemberInfoProvider");
  return ctx;
}; 