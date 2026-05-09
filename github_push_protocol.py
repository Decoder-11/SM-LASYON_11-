#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
GITHUB PUSH VE DOĞRULAMA PROTOKOLÜ
================================================================================
Tarih: 2026-05-08
Amaç: Simülasyon-11 GitHub deposuna dosya yükleme ve doğrulama
Kullanım: python github_push_protocol.py
================================================================================
"""

import os
import sys
import subprocess
from datetime import datetime

# Türkçe UTF-8 desteği
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


class GitHubProtocol:
    """GitHub push protokolü."""

    @staticmethod
    def check_git_status():
        """Git durumunu kontrol et."""
        print("\n📊 Git Durumu Kontrol Ediliyor...\n")

        result = subprocess.run(
            ['git', 'status', '--short'],
            cwd='.',
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            if result.stdout:
                print("✏️  Değişiklikler Algılandı:\n")
                print(result.stdout)
            else:
                print("✅ Çalışma klasörü temiz (hiçbir değişiklik yok)\n")
        else:
            print("❌ Git komutu başarısız oldu!")
            return False

        return True

    @staticmethod
    def list_modified_files():
        """Değiştirilmiş dosyaları listele."""
        result = subprocess.run(
            ['git', 'diff', '--name-only'],
            cwd='.',
            capture_output=True,
            text=True
        )

        if result.stdout:
            print("📝 Değiştirilmiş Dosyalar:\n")
            for file in result.stdout.strip().split('\n'):
                if file:
                    print(f"  • {file}")
            return result.stdout.strip().split('\n')

        return []

    @staticmethod
    def add_all_changes():
        """Tüm değişiklikleri ekle."""
        print("\n➕ Tüm Değişiklikler Ekleniyor...\n")

        result = subprocess.run(
            ['git', 'add', '.'],
            cwd='.',
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✅ Değişiklikler Git indeksine eklendi\n")
            return True
        else:
            print(f"❌ Hata: {result.stderr}\n")
            return False

    @staticmethod
    def commit_with_message(message: str):
        """Mesajla commit et."""
        print(f"\n💾 Commit Ediliyor: '{message}'\n")

        result = subprocess.run(
            ['git', 'commit', '-m', message],
            cwd='.',
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✅ Commit başarıyla oluşturuldu\n")
            print(result.stdout)
            return True
        else:
            print(f"❌ Commit hatası: {result.stderr}\n")
            return False

    @staticmethod
    def push_to_remote(branch: str = 'main'):
        """Remote'a push et."""
        print(f"\n🚀 {branch} Dalına Push Ediliyor...\n")

        result = subprocess.run(
            ['git', 'push', 'origin', branch],
            cwd='.',
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✅ Push başarıyla tamamlandı\n")
            print(result.stdout)
            return True
        else:
            print(f"❌ Push hatası: {result.stderr}\n")
            return False

    @staticmethod
    def full_workflow(commit_message: str):
        """Tam GitHub iş akışı."""
        print("=" * 80)
        print("GITHUB PUSH PROTOKOLÜ - TAM İŞ AKIŞI")
        print("=" * 80)

        # Adım 1: Durumu kontrol et
        if not GitHubProtocol.check_git_status():
            return False

        # Adım 2: Değiştirilmiş dosyaları listele
        modified_files = GitHubProtocol.list_modified_files()

        if not modified_files or all(f == '' for f in modified_files):
            print("⏭️  Hiçbir değişiklik yok, atlanıyor...\n")
            return True

        # Adım 3: Tüm değişiklikleri ekle
        if not GitHubProtocol.add_all_changes():
            return False

        # Adım 4: Commit et
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"{commit_message} [{timestamp}]"

        if not GitHubProtocol.commit_with_message(full_message):
            return False

        # Adım 5: Push et
        if not GitHubProtocol.push_to_remote():
            return False

        print("=" * 80)
        print("✅ TÜMLEME BAŞARILI")
        print("=" * 80 + "\n")
        return True


# ÖNCEDEN TANIMLANMIŞ PUSH MESAJLARI
PUSH_MESSAGES = {
    "doğrulama": "📊 Doğrulama Testleri ve Validasyon Raporu Eklendi",
    "keşif": "🔬 Yeni Bilimsel Keşif Modülü Entegre Edildi",
    "düzeltme": "🔧 Hata Düzeltmeleri ve Optimizasyon",
    "sentez": "🧬 Yeni Sentez Keşifler Eklendi",
    "api": "🌐 NASA API Entegrasyonu Güncellemesi",
    "dokümantasyon": "📚 Dokümantasyon ve README Güncellemeleri",
    "test": "🧪 Test Kütüphanesi Genişletmeleri",
    "github": "🚀 GitHub İş Akışı Optimizasyonu"
}


def main():
    """Ana fonksiyon."""
    import argparse

    parser = argparse.ArgumentParser(
        description="GitHub Push Protokolü - Simülasyon-11 Deposu"
    )
    parser.add_argument(
        'type',
        nargs='?',
        default='keşif',
        choices=list(PUSH_MESSAGES.keys()),
        help='Push türü'
    )
    parser.add_argument(
        '--message', '-m',
        type=str,
        help='Özel commit mesajı'
    )
    parser.add_argument(
        '--branch', '-b',
        type=str,
        default='main',
        help='Hedef dal'
    )
    parser.add_argument(
        '--check-only',
        action='store_true',
        help='Sadece durumu kontrol et, push etme'
    )

    args = parser.parse_args()

    # Mesaj seç
    if args.message:
        message = args.message
    else:
        message = PUSH_MESSAGES.get(args.type, PUSH_MESSAGES['keşif'])

    # Sadece kontrol modu
    if args.check_only:
        print("\n🔍 Sadece Kontrol Modu Açık\n")
        GitHubProtocol.check_git_status()
        GitHubProtocol.list_modified_files()
        return

    # Tam iş akışı
    GitHubProtocol.full_workflow(message)


if __name__ == "__main__":
    main()

