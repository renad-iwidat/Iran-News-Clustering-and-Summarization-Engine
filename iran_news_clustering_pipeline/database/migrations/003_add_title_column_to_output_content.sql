-- Migration: Add title column to output_content table
-- Description: Adds a title field to store generated headlines for reports

ALTER TABLE output_content 
ADD COLUMN IF NOT EXISTS title VARCHAR(500);

-- Add comment
COMMENT ON COLUMN output_content.title IS 'Generated headline/title for the report content';
