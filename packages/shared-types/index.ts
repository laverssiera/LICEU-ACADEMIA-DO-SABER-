export type UUID = string;

export interface PlatformStatus {
  platform: string;
  version: string;
  status: "running" | "degraded" | "stopped";
}
