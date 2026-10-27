/**
 * Shared TypeScript types mirroring packages/shared/openapi.yaml.
 * Keep in sync manually until codegen is wired (contract changes via Orchestrator only).
 */

export type Severity = 'info' | 'low' | 'medium' | 'high' | 'critical';

export type Verdict =
  | 'VERIFIED_SAFE'
  | 'LOW_RISK'
  | 'MODERATE_RISK'
  | 'HIGH_RISK'
  | 'DANGEROUS'
  | 'PENDING';

export type SourceType = 'github' | 'npm' | 'pypi' | 'docker' | 'remote_url';

export type CategoryKey =
  | 'secrets_exfil'
  | 'malware_exec'
  | 'supply_chain'
  | 'prompt_injection'
  | 'capability_excess'
  | 'protocol_reliability'
  | 'compliance'
  | 'community';

export interface SourceRef {
  type: SourceType;
  locator: string;
  ref?: string;
}

export interface VerdictResult {
  source: SourceRef;
  known: boolean;
  verdict?: Verdict;
  riskScore?: number | null;
  versionId?: string | null;
  pinnedRef?: string | null;
  quarantined?: boolean;
  block: boolean;
  warn: boolean;
  reason?: string;
  checkedAt?: string;
}

export interface ToolSpec {
  name: string;
  description?: string;
  inputSchema?: Record<string, unknown>;
}

/** risk_score convention (D-2): 0-100, HIGHER = RISKIER. trust = 100 - risk is display-only. */
export const riskToTrust = (risk: number): number => 100 - risk;
