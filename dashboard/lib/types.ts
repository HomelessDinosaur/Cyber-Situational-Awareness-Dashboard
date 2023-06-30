export type DataMode = "realtime" | "highrisk";

export interface StixObject {
  type: string;
  spec_version: string;
  id: string;
  created: string;
  modified: string;
}

export interface Ipv4Address extends StixObject {
  value: string;
}

export interface NetworkTraffic {
  start: string;
  end: string;
  is_active: boolean;
  src_ref: string;
  dst_ref: string;
  src_port: number;
  dst_port: number;
  protocols: string[];
}

export interface Infrastructure extends StixObject {
  name: string;
  description: string;
  infrastructure_types: string[];
  aliases: string[];
  kill_chain_phases: string[];
  first_seen: string;
  last_seen: string;
}

export interface Relationship extends StixObject {
  relationship_type: string;
  source_ref: string;
  target_ref: string;
}

export interface Sighting extends StixObject {
  description?: string;
  first_seen: string;
  last_seen?: string;
  count?: number;
  sighting_of_ref: string;
  observed_data_refs?: string[];
  where_sighted_refs?: string[];
  summary?: boolean;
}

export interface Location extends StixObject {
  country: string;
}

export interface Indicator extends StixObject {
  name?: string;
  description?: string;
  indicator_types?: string[];
  pattern: string;
  pattern_type: string;
  pattern_version?: string;
  valid_from: string;
  valid_until?: string;
  kill_chain_phases?: string[];
}
