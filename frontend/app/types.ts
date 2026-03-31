export type Job = {
  id: number;
  title: string;
  company: string;
  description: string;
  url: string | null;
  score: number | null;
  fit_reasoning: string | null;
  status: string;
  created_at: string;
};
