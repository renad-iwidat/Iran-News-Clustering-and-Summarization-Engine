-- Migration 005: Migrate existing translation data from raw_data to translations table
-- This migration copies all existing translation data to the new translations table

-- Insert existing translations into the new table
INSERT INTO translations (
    raw_data_id,
    target_language,
    original_language,
    translated_content,
    translation_status,
    translated_at,
    translation_error_message,
    created_at
)
SELECT 
    id as raw_data_id,
    'ar' as target_language,
    original_language,
    arabic_content as translated_content,
    translation_status,
    translated_at,
    translation_error_message,
    COALESCE(translated_at, CURRENT_TIMESTAMP) as created_at
FROM raw_data
WHERE original_language IS NOT NULL
ON CONFLICT (raw_data_id, target_language) DO NOTHING;

-- Verify migration
DO $$
DECLARE
    raw_data_count INTEGER;
    translations_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO raw_data_count FROM raw_data WHERE original_language IS NOT NULL;
    SELECT COUNT(*) INTO translations_count FROM translations;
    
    RAISE NOTICE 'Migration completed:';
    RAISE NOTICE '  - raw_data records with translations: %', raw_data_count;
    RAISE NOTICE '  - translations records created: %', translations_count;
END $$;
