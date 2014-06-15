#ifndef IMPORT_H_INCLUDED
#define IMPORT_H_INCLUDED

/** gettimeofday */
/* Win32 gettimeofday implementation from
http://social.msdn.microsoft.com/Forums/vstudio/en-US/430449b3-f6dd-4e18-84de-eebd26a8d668/gettimeofday
with a missing "0" added to DELTA_EPOCH_IN_MICROSECS */

#ifdef _WIN32
#include <time.h>
#include <windows.h>
#if defined(_MSC_VER) || defined(_MSC_EXTENSIONS)
#define DELTA_EPOCH_IN_MICROSECS  116444736000000000Ui64
#else
#define DELTA_EPOCH_IN_MICROSECS  116444736000000000ULL
#endif


#include <sys/time.h>
#include <unistd.h>

//struct timezone;
//
//int gettimeofday(struct timeval *tv, struct timezone *tz)
//{
//	FILETIME ft;
//	unsigned __int64 tmpres = 0;
//
//  (void)tz;
//
//	if (NULL != tv)
//	{
//		GetSystemTimeAsFileTime(&ft);
//
//		tmpres |= ft.dwHighDateTime;
//		tmpres <<= 32;
//		tmpres |= ft.dwLowDateTime;
//
//		/*converting file time to unix epoch*/
//		tmpres -= DELTA_EPOCH_IN_MICROSECS;
//		tmpres /= 10;  /*convert into microseconds*/
//		tv->tv_sec = (long)(tmpres / 1000000UL);
//		tv->tv_usec = (long)(tmpres % 1000000UL);
//	}
//
//	return 0;
//}
#else
#include <sys/time.h>
#endif

#endif // IMPORT_H_INCLUDED
