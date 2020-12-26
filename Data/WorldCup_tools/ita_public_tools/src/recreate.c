/*
 
          Copyright (C) 1997, 1998, 1999 Hewlett-Packard Company
                         ALL RIGHTS RESERVED.
 
  The enclosed software and documentation includes copyrighted works
  of Hewlett-Packard Co. For as long as you comply with the following
  limitations, you are hereby authorized to (i) use, reproduce, and
  modify the software and documentation, and to (ii) distribute the
  software and documentation, including modifications, for
  non-commercial purposes only.
      
  1.  The enclosed software and documentation is made available at no
      charge in order to advance the general development of
      the Internet, the World-Wide Web, and Electronic Commerce.
 
  2.  You may not delete any copyright notices contained in the
      software or documentation. All hard copies, and copies in
      source code or object code form, of the software or
      documentation (including modifications) must contain at least
      one of the copyright notices.
 
  3.  The enclosed software and documentation has not been subjected
      to testing and quality control and is not a Hewlett-Packard Co.
      product. At a future time, Hewlett-Packard Co. may or may not
      offer a version of the software and documentation as a product.
  
  4.  THE SOFTWARE AND DOCUMENTATION IS PROVIDED "AS IS".
      HEWLETT-PACKARD COMPANY DOES NOT WARRANT THAT THE USE,
      REPRODUCTION, MODIFICATION OR DISTRIBUTION OF THE SOFTWARE OR
      DOCUMENTATION WILL NOT INFRINGE A THIRD PARTY'S INTELLECTUAL
      PROPERTY RIGHTS. HP DOES NOT WARRANT THAT THE SOFTWARE OR
      DOCUMENTATION IS ERROR FREE. HP DISCLAIMS ALL WARRANTIES,
      EXPRESS AND IMPLIED, WITH REGARD TO THE SOFTWARE AND THE
      DOCUMENTATION. HP SPECIFICALLY DISCLAIMS ALL WARRANTIES OF
      MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
  
  5.  HEWLETT-PACKARD COMPANY WILL NOT IN ANY EVENT BE LIABLE FOR ANY
      DIRECT, INDIRECT, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES
      (INCLUDING LOST PROFITS) RELATED TO ANY USE, REPRODUCTION,
      MODIFICATION, OR DISTRIBUTION OF THE SOFTWARE OR DOCUMENTATION.
 
*/
/**************************************************************************/
/* RECREATE.C                                                             */
/* This program recreates the Common Log Format from the reduced binary   */
/* log format.                                                            */
/**************************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "inttypes.h"
#include "definitions.h"
#include "endian.h"
#include "request.h"

#define NUM_ENTRIES 90000

char *ObjectNames[NUM_ENTRIES];
FILE *object_mappings;

int PrintLog = TRUE;
uint32_t TotalRequests = 0;
double TotalBytes = 0.0;
uint32_t MaxObject = 0;
uint32_t MaxClient = 0;
uint32_t StartTime;
uint32_t LastTime = 0;
int OutOfOrder = 0;
int Endian = NO_ENDIAN;

/**************************************************************************/
/* DEFINITIONS                                                            */
/**************************************************************************/

const int INTERVAL = 60;
uint32_t nextInterval = 0;
uint32_t requestCount = 0;
long totalBytes = 0;

/**************************************************************************/
/* READ LOG                                                               */
/**************************************************************************/
void ReadLog()
{
  struct request BER, LER, *R;
  int value;
  int count = 0;
  time_t ts;
  struct tm *time_info;
  char date[1024], day[10], hour[10], month[10], min[10];

  /* status indicator */
  fprintf(stderr, "Reading Access Log\n");

  /* read the initial request */
  if ((fread(&BER, sizeof(struct request), 1, stdin)) != 1)
  {
    fprintf(stderr, "Error: Failed to read initial request!\n");
    exit(-1);
  }

  switch (Endian)
  {
  case LITTLE_ENDIAN:
    LittleEndianRequest(&BER, &LER);
    R = &LER;
    break;

  case BIG_ENDIAN:
    R = &BER;
    break;

  default:
    fprintf(stderr, "Error: unknown Endian!\n");
    exit(-1);
  }

  /* save start time */
  StartTime = R->timestamp;
  nextInterval = StartTime + INTERVAL;

  /* read through access log */
  while ((!feof(stdin)) && (1))
  {
    /* status indicator */
    if (count % 1000000 == 0)
      fprintf(stderr, "%d\n", count);
    count++;

    // Count request in interval
    requestCount++;
    /* update statistics */
    TotalRequests++;
    // Count bytes in interval
    if (R->size != NO_SIZE)
    {
      TotalBytes += R->size;
      totalBytes += R->size;
    }

    /* check timestamp */
    if (R->timestamp < LastTime)
      OutOfOrder++;

    /* update last time */
    LastTime = R->timestamp;

    if (R->timestamp >= nextInterval)
    {
      /* determine timestamp info */
      ts = (time_t)R->timestamp;
      time_info = gmtime(&ts);

      if (time_info->tm_min < 10)
        sprintf(min, "0%d", time_info->tm_min);
      else
        sprintf(min, "%d", time_info->tm_min);

      if (time_info->tm_hour < 10)
        sprintf(hour, "0%d", time_info->tm_hour);
      else
        sprintf(hour, "%d", time_info->tm_hour);

      if (time_info->tm_mon < 9)
        sprintf(month, "0%d", (time_info->tm_mon + 1));
      else
        sprintf(month, "%d", (time_info->tm_mon + 1));

      if (time_info->tm_mday < 10)
        sprintf(day, "0%d", time_info->tm_mday);
      else
        sprintf(day, "%d", time_info->tm_mday);

      sprintf(date, "%s/%s:%s:%s",
              day, month, hour, min);

      /* print info in Common Log Format */
      fprintf(stdout, "%u,%s,%u,%d\n", R->timestamp, date, requestCount, totalBytes);

      nextInterval += INTERVAL;
      requestCount = 0;
      totalBytes = 0;
    }

    /* read the next request */
    value = fread(&BER, sizeof(struct request), 1, stdin);

    if (value == 1)
    {
      switch (Endian)
      {
      case LITTLE_ENDIAN:
        LittleEndianRequest(&BER, &LER);
        R = &LER;
        break;

      case BIG_ENDIAN:
        R = &BER;
        break;

      default:
        fprintf(stderr, "Error: unknown Endian!\n");
        exit(-1);
      }
    }
  }

  /* final count */
  fprintf(stderr, "%d\n", count);
}

/**************************************************************************/
/* PRINT RESULTS                                                          */
/**************************************************************************/
void PrintResults()
{
  /* status indicator */
  fprintf(stderr, "Printing Results\n");

  fprintf(stderr, "    Total Requests: %u\n", TotalRequests);
  fprintf(stderr, "       Total Bytes: %.0f\n", TotalBytes);
  fprintf(stderr, "Mean Transfer Size: %f\n",
          TotalBytes / (double)TotalRequests);
  fprintf(stderr, "     Max Client ID: %u\n", MaxClient);
  fprintf(stderr, "     Max Object ID: %u\n", MaxObject);

  fprintf(stderr, "        Start Time: %u\n", StartTime);
  fprintf(stderr, "       Finish Time: %u\n", LastTime);
  fprintf(stderr, "      Out of Order: %d\n", OutOfOrder);
}

/**************************************************************************/
/* INITIALIZE                                                             */
/**************************************************************************/
void Initialize(int argc, char **argv)
{
  int i, ID, value;
  char nextline[8192], name[8192];

  /* check command line */
  if (argc != 2)
  {
    fprintf(stderr, "usage: %s file_mappings\n", argv[0]);
    exit(-1);
  }

  /* status indicator */
  fprintf(stderr, "Initializing\n");

  /* determine which endian platform uses */
  Endian = CheckEndian();

  /* open input file of object mappings */
  if ((object_mappings = fopen(argv[1], "r")) == NULL)
  {
    fprintf(stderr, "Error: failed to open %s\n", argv[1]);
    exit(-1);
  }

  /* initialize array of names */
  for (i = 0; i < NUM_ENTRIES; i++)
    ObjectNames[i] = NULL;

  /* read in names */
  fgets(nextline, 8192, object_mappings);

  while (!feof(object_mappings))
  {
    value = sscanf(nextline, "%d %s", &ID, name);

    if ((value == 2) && (ID >= 0) && (ID < NUM_ENTRIES))
    {
      if ((ObjectNames[ID] = (char *)malloc(strlen(name) + 2)) == NULL)
      {
        fprintf(stderr, "Error: malloc failed!\n");
        exit(-1);
      }

      /* store the name */
      strcpy(ObjectNames[ID], name);
    }

    else if ((value == 2) && (ID >= NUM_ENTRIES))
    {
      fprintf(stderr, "Error: Name array is too small! (%d)\n",
              ID);
      exit(-1);
    }

    fgets(nextline, 8192, object_mappings);
  }
}

/**************************************************************************/
/* TERMINATE                                                              */
/**************************************************************************/
void Terminate()
{
  int i;

  /* status indicator */
  fprintf(stderr, "Terminating\n");

  /* close data files */
  fclose(object_mappings);

  /* clean up array of names */
  for (i = 0; i < NUM_ENTRIES; i++)
  {
    if (ObjectNames[i] != NULL)
    {
      free(ObjectNames[i]);
      ObjectNames[i] = NULL;
    }
  }
}

/**************************************************************************/
/* MAIN PROGRAM                                                           */
/**************************************************************************/
int main(int argc, char **argv)
{
  Initialize(argc, argv);

  ReadLog();

  // PrintResults();

  Terminate();

  return (0);
}
