import { createClient } from "@supabase/supabase-js";

const SUPABASE_URL = "https://evxchpvtxienefjtcbhs.supabase.co"; 
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV2eGNocHZ0eGllbmVmanRjYmhzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDAyNDUzMTMsImV4cCI6MjA1NTgyMTMxM30.AT95PWkDSPUBQAQCmE1VZrhIltvOuj4moE34pRs3OVw"; 

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
