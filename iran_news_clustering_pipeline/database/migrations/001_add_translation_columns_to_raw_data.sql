-- Migration: Add translation-related columns to raw_data table
-- Purpose: Store translated content and track translation status
-- Date: 2024
-- Description: This migration adds columns to support Arabic translation workflow
--              where Hebrew news are translated to Arabic and Arabic news remain as-is

-- Add column to store the detected original language of the news article
-- Values: 'ar' for Arabic, 'he' for Hebrew
ALTER TABLE raw_data 
ADD COLUMN IF NOT EXISTS original_language VARCHAR(10);

-- Add column to store the Arabic version of the content
-- For Arabic news: copy of original content
-- For Hebrew news: translated content
ALTER TABLE raw_data 
ADD COLUMN IF NOT EXISTS arabic_content TEXT;

-- Add column to track the translation status
-- Values: 
--   'not_required' - Article is already in Arabic
--   'pending' - Article needs translation (Hebrew)
--   'in_progress' - Translation is currently being processed
--   'completed' - Translation completed successfully
--   'failed' - Translation failed (will retry later)
ALTER TABLE raw_data 
ADD COLUMN IF NOT EXISTS translation_status VARCHAR(20) DEFAULT 'pending';

-- Add column to store when the translation was completed
ALTER TABLE raw_data 
ADD COLUMN IF NOT EXISTS translated_at TIMESTAMP WITH TIME ZONE;

-- Add column to store translation error message if translation fails
ALTER TABLE raw_data 
ADD COLUMN IF NOT EXISTS translation_error_message TEXT;

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_raw_data_translation_status 
ON raw_data(translation_status);

CREATE INDEX IF NOT EXISTS idx_raw_data_original_language 
ON raw_data(original_language);

CREATE INDEX IF NOT EXISTS idx_raw_data_is_processed_and_translation_status 
ON raw_data(is_processed, translation_status);

-- Add comment to table for documentation
COMMENT ON COLUMN raw_data.original_language IS 'Original language of the news article (ar=Arabic, he=Hebrew)';
COMMENT ON COLUMN raw_data.arabic_content IS 'Arabic version of the content (original or translated)';
COMMENT ON COLUMN raw_data.translation_status IS 'Status of translation process (not_required, pending, in_progress, completed, failed)';
COMMENT ON COLUMN raw_data.translated_at IS 'Timestamp when translation was completed';
COMMENT ON COLUMN raw_data.translation_error_message IS 'Error message if translation failed';
