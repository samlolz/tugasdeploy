"""
FITURBERITA/tests.py
Unit tests untuk aplikasi FITURBERITA
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import BERITA, Komentar
from datetime import datetime


class BERITAModelTest(TestCase):
    """Test case untuk model BERITA"""
    
    def setUp(self):
        """Setup test data"""
        self.BERITA = BERITA.objects.create(
            judul="Test BERITA",
            isi_BERITA="Ini adalah isi BERITA untuk testing"
        )
    
    def test_BERITA_creation(self):
        """Test pembuatan BERITA"""
        self.assertTrue(isinstance(self.BERITA, BERITA))
        self.assertEqual(self.BERITA.__str__(), self.BERITA.judul)
    
    def test_BERITA_jumlah_komentar(self):
        """Test method get_jumlah_komentar"""
        # Awalnya tidak ada komentar
        self.assertEqual(self.BERITA.get_jumlah_komentar(), 0)
        
        # Tambah komentar
        Komentar.objects.create(
            nama="Test User",
            isi_komentar="Test Komentar",
            BERITA=self.BERITA
        )
        
        self.assertEqual(self.BERITA.get_jumlah_komentar(), 1)


class KomentarModelTest(TestCase):
    """Test case untuk model Komentar"""
    
    def setUp(self):
        """Setup test data"""
        self.BERITA = BERITA.objects.create(
            judul="Test BERITA",
            isi_BERITA="Ini adalah isi BERITA untuk testing"
        )
        self.komentar = Komentar.objects.create(
            nama="Test User",
            isi_komentar="Test Komentar",
            BERITA=self.BERITA
        )
    
    def test_komentar_creation(self):
        """Test pembuatan komentar"""
        self.assertTrue(isinstance(self.komentar, Komentar))
        self.assertEqual(self.komentar.BERITA, self.BERITA)
    
    def test_komentar_str(self):
        """Test string representation"""
        expected = f"Komentar oleh {self.komentar.nama} pada {self.BERITA.judul}"
        self.assertEqual(str(self.komentar), expected)


class BERITAAPITest(APITestCase):
    """Test case untuk BERITA API endpoints"""
    
    def setUp(self):
        """Setup test data dan client"""
        self.client = APIClient()
        self.BERITA_data = {
            'judul': 'Test BERITA API',
            'isi_BERITA': 'Ini adalah isi BERITA dari API test'
        }
        self.BERITA = BERITA.objects.create(**self.BERITA_data)
    
    def test_get_all_BERITA(self):
        """Test GET request untuk list BERITA"""
        response = self.client.get(reverse('BERITA-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_single_BERITA(self):
        """Test GET request untuk detail BERITA"""
        response = self.client.get(
            reverse('BERITA-detail', kwargs={'pk': self.BERITA.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['judul'], self.BERITA.judul)
    
    def test_create_BERITA(self):
        """Test POST request untuk create BERITA"""
        new_BERITA = {
            'judul': 'BERITA Baru',
            'isi_BERITA': 'Ini BERITA baru dari test'
        }
        response = self.client.post(
            reverse('BERITA-list'),
            new_BERITA,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BERITA.objects.count(), 2)
    
    def test_update_BERITA(self):
        """Test PUT request untuk update BERITA"""
        updated_data = {
            'judul': 'Judul Updated',
            'isi_BERITA': 'Isi BERITA updated'
        }
        response = self.client.put(
            reverse('BERITA-detail', kwargs={'pk': self.BERITA.pk}),
            updated_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.BERITA.refresh_from_db()
        self.assertEqual(self.BERITA.judul, 'Judul Updated')
    
    def test_delete_BERITA(self):
        """Test DELETE request untuk hapus BERITA"""
        response = self.client.delete(
            reverse('BERITA-detail', kwargs={'pk': self.BERITA.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BERITA.objects.count(), 0)
    
    def test_search_BERITA(self):
        """Test search functionality"""
        response = self.client.get(
            reverse('BERITA-list'),
            {'search': 'Test'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)


class KomentarAPITest(APITestCase):
    """Test case untuk Komentar API endpoints"""
    
    def setUp(self):
        """Setup test data dan client"""
        self.client = APIClient()
        self.BERITA = BERITA.objects.create(
            judul='Test BERITA',
            isi_BERITA='Isi BERITA test'
        )
        self.komentar_data = {
            'nama': 'Test User',
            'isi_komentar': 'Test komentar',
            'BERITA': self.BERITA.pk
        }
        self.komentar = Komentar.objects.create(
            nama=self.komentar_data['nama'],
            isi_komentar=self.komentar_data['isi_komentar'],
            BERITA=self.BERITA
        )
    
    def test_get_all_komentar(self):
        """Test GET request untuk list komentar"""
        response = self.client.get(reverse('komentar-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_komentar(self):
        """Test POST request untuk create komentar"""
        new_komentar = {
            'nama': 'User Baru',
            'isi_komentar': 'Komentar baru',
            'BERITA': self.BERITA.pk
        }
        response = self.client.post(
            reverse('komentar-list'),
            new_komentar,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Komentar.objects.count(), 2)
    
    def test_filter_komentar_by_BERITA(self):
        """Test filter komentar berdasarkan BERITA"""
        response = self.client.get(
            reverse('komentar-list'),
            {'BERITA': self.BERITA.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_komentar_from_BERITA_endpoint(self):
        """Test custom action untuk get komentar dari BERITA"""
        response = self.client.get(
            reverse('BERITA-komentar', kwargs={'pk': self.BERITA.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['jumlah_komentar'], 1)