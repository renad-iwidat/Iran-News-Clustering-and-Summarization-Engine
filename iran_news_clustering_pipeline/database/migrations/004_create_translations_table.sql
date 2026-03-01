-- Migration 004: Create translations table
-- Separates translation data from raw_data table for better organization and performance

-- Create translations table
CREATE TABLE IF NOT EXISTS translations (
    id SERIAL PRIMARY KEY,
    raw_data_id INTEGER NOT NULL REFERENCES raw_data(id) ON DELETE CASCADE,
    target_language VARCHAR(10) NOT NULL DEFAULT 'ar',
    original_language VARCHAR(10),
    translated_content TEXT,
    translation_status VARCHAR(50) DEFAULT 'pending',
    translated_at TIMESTAMP,
    translation_error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(raw_data_id, target_language)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_translations_raw_data_id ON translations(raw_data_id);
CREATE INDEX IF NOT EXISTS idx_translations_status ON translations(translation_status);
CREATE INDEX IF NOT EXISTS idx_translations_target_language ON translations(target_language);

-- Add comments for documentation
COMMENT ON TABLE translations IS 'Stores translations of news articles from raw_data table';
COMMENT ON COLUMN translations.raw_data_id IS 'Foreign key to raw_data table';
COMMENT ON COLUMN translations.target_language IS 'Target language code (ar=Arabic, en=English, etc.)';
COMMENT ON COLUMN translations.original_language IS 'Original language detected (ar=Arabic, he=Hebrew)';
COMMENT ON COLUMN translations.translated_content IS 'The translated content in target language';
COMMENT ON COLUMN translations.translation_status IS 'Status: pending, completed, not_required, failed';
