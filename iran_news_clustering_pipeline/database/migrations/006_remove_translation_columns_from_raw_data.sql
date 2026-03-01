-- Migration 006: Remove translation columns from raw_data table
-- These columns are now stored in the translations table

-- Drop translation-related columns from raw_data
ALTER TABLE raw_data DROP COLUMN IF EXISTS arabic_content;
ALTER TABLE raw_data DROP COLUMN IF EXISTS original_language;
ALTER TABLE raw_data DROP COLUMN IF EXISTS translation_status;
ALTER TABLE raw_data DROP COLUMN IF EXISTS translated_at;
ALTER TABLE raw_data DROP COLUMN IF EXISTS translation_error_message;

-- Verify cleanup
DO $$
BEGIN
    RAISE NOTICE 'Migration completed: Removed translation columns from raw_data table';
    RAISE NOTICE 'Translation data is now stored in the translations table';
END $$;
